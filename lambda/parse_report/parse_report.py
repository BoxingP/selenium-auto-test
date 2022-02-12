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
        for stage in [test['setup'], test['call'], test['teardown']]:
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


def lambda_handler(event, context):
    failed_tests = get_failed_tests(event)
    return generate_notification_msg(failed_tests)
