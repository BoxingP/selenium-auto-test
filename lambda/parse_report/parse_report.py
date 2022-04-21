import json
import os
import re
import urllib.request
from string import Template

import boto3

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')


def generate_notification_msg(failed_tests: list):
    content = ''
    index = 1
    for test in failed_tests:
        sentence = ''
        if len(failed_tests) != 1:
            sentence = str(index) + '\n'
        for key, value in test.items():
            sentence = sentence + '%s: %s\n' % (key.upper(), value)
        content = content + '\n%s' % sentence
        index += 1
    message = f"Failed tests:\n{content}\nPlease check the details in the Allure report:\nhttp://{os.environ['allure_report_endpoint']}"
    return message


def get_latest_file(key_word: str, s3_bucket=os.environ['s3_bucket_name'], target_dir='') -> str:
    client = boto3.client('s3')
    objects = []
    paginator = client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=s3_bucket, Prefix=target_dir)
    for obj in page_iterator.search(f'Contents[?contains(Key, `{key_word}`)][]'):
        if not obj['Key'].endswith('/'):
            objects.append(obj['Key'])
    objects.sort()
    if objects:
        return objects[-1]
    else:
        return ''


def get_date(string: str) -> int:
    try:
        return int(re.search('_([0-9]+).', string).group(1))
    except AttributeError:
        return 0


def get_screenshot_url(test_name: str, s3_bucket=os.environ['s3_bucket_name'], screenshots_dir='') -> str:
    client = boto3.client('s3')
    location = client.get_bucket_location(Bucket=s3_bucket)['LocationConstraint']
    screenshot_name = get_latest_file(key_word=test_name, target_dir=screenshots_dir)
    screenshot_date = get_date(screenshot_name)
    start_flag = get_date(get_latest_file(key_word='last_run_utc', target_dir=screenshots_dir))

    if screenshot_date:
        if screenshot_date > start_flag:
            return f'https://{s3_bucket}.s3.{location}.amazonaws.com.cn/{screenshot_name}'
    return ''


def get_failed_tests(json_data):
    failed_tests = []
    for test in json_data:
        if test['outcome'] == 'passed':
            continue
        name = '::'.join(test['name'].split('::')[-2:])
        stage_outcome = []
        stage_detail = []
        for key in ('name', 'duration', 'run_index', 'outcome'):
            test.pop(key, None)
        for stage in test.values():
            if stage['outcome'] == 'passed':
                continue
            stage_outcome.append('%s %s' % (stage['name'], stage['outcome']))
            detail = ''
            for key in [key for key in list(stage.keys()) if key not in ('name', 'duration', 'outcome')]:
                detail = detail + '\n    %s' % stage[key]
            stage_detail.append('\n  %s: %s' % (stage['name'], detail))

        summary = ', '.join(stage_outcome)
        screenshot_url = ''
        if 'call' in summary:
            screenshot_url = get_screenshot_url(test_name=name.split('::')[1], screenshots_dir='screenshots')
        detail = '  '.join(stage_detail)

        failed_tests.append({'name': name, 'reason': summary, 'screenshot': screenshot_url, 'error': detail})

    return failed_tests


def send_alarm_info(failed_tests):
    with open(CONFIG_PATH, 'r', encoding='UTF-8') as file:
        config = json.load(file)
    url = config['url']
    alarm_template = Template(config['alarm_template'])
    response = []
    for test in failed_tests:
        alarm = json.loads(alarm_template.substitute(target_name=test['name'], message=test['reason']))
        params = json.dumps(alarm).encode('utf8')
        req = urllib.request.Request(url, data=params, headers={'content-type': 'application/json'})
        resource = urllib.request.urlopen(req)
        content = resource.read().decode(resource.headers.get_content_charset())
        response.append(content)
    return '\n'.join(response)


def lambda_handler(event, context):
    failed_tests = get_failed_tests(event)
    response = ''
    send_alarm_error_msg = ''
    message = ''
    generate_message_error_msg = ''
    try:
        response = send_alarm_info(failed_tests)
    except Exception as error:
        send_alarm_error_msg = repr(error)
    try:
        message = generate_notification_msg(failed_tests)
    except Exception as error:
        generate_message_error_msg = repr(error)

    result = {
        'alarm': {
            'response': response,
            'exception': send_alarm_error_msg
        },
        'notification': {
            'message': message,
            'exception': generate_message_error_msg
        }
    }
    return result
