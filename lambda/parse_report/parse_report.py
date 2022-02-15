import json
import os
import urllib.request
from string import Template

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
    message = 'Failed tests:\n{}\nPlease check the details in the Allure report.'.format(content)
    return message


def get_failed_tests(json_data):
    failed_tests = []
    for test in json_data:
        if test['outcome'] == 'passed':
            continue
        name = '::'.join(test['name'].split("::")[-2:])
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
        detail = '  '.join(stage_detail)

        failed_tests.append({'name': name, 'reason': summary, 'error': detail})

    return failed_tests


def send_alarm_info(failed_tests):
    with open(CONFIG_PATH, 'r', encoding='UTF-8') as file:
        config = json.load(file)
    url = config['url']
    alarm_template = Template(config['alarm_template'])
    for test in failed_tests:
        alarm = json.loads(alarm_template.substitute(target_name=test['name'], message=test['reason']))
        params = json.dumps(alarm).encode('utf8')
        req = urllib.request.Request(url, data=params, headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(req)


def lambda_handler(event, context):
    failed_tests = get_failed_tests(event)
    send_alarm_info(failed_tests)
    return generate_notification_msg(failed_tests)
