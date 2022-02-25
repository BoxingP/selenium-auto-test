from aws_cdk import (
    aws_events as events,
    aws_events_targets as targets,
    aws_lambda as _lambda,
    aws_sns as sns,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfn_tasks,
    core as cdk
)


class SchedulerStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        test_website_job = sfn_tasks.LambdaInvoke(
            self, 'TestWebsite',
            lambda_function=_lambda.Function.from_function_arn(
                self, 'TestWebsiteLambda',
                function_arn=cdk.Fn.import_value(
                    construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'TestWebsiteLambdaArn'
                )
            ),
            result_path='$',
            result_selector={
                'report.$': '$.Payload.report'
            },
            timeout=cdk.Duration.minutes(5)
        )

        generate_report_job = sfn_tasks.LambdaInvoke(
            self, 'GenerateReport',
            lambda_function=_lambda.Function.from_function_arn(
                self, 'GenerateReportLambda',
                function_arn=cdk.Fn.import_value(
                    construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'GenerateReportLambdaArn'
                )
            ),
            result_path=sfn.JsonPath.DISCARD,
            timeout=cdk.Duration.minutes(5)
        )

        parse_report_job = sfn_tasks.LambdaInvoke(
            self, 'ParseReport',
            lambda_function=_lambda.Function.from_function_arn(
                self, 'ParseReportLambda',
                function_arn=cdk.Fn.import_value(
                    construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'ParseReportLambdaArn'
                )
            ),
            result_path='$',
            result_selector={
                'alarm.$': '$.Payload.alarm',
                'notification.$': '$.Payload.notification'
            }
        )

        send_notification_job = sfn_tasks.SnsPublish(
            self, 'SendNotification',
            topic=sns.Topic.from_topic_arn(
                self, 'SendNotificationTopic',
                topic_arn=cdk.Fn.import_value(
                    construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'SnsTopicArn'
                )
            ),
            message=sfn.TaskInput.from_json_path_at("$.message"),
            subject='There Are Failed Tests Occurred on the Website',
            input_path='$.notification',
            result_path='$'
        )

        job_succeeded = sfn.Succeed(self, 'JobIsSucceeded')

        is_sent_notification = sfn.Choice(self, 'DecideWhetherSendNotification', output_path='$.report.tests')
        is_sent_notification.when(
            sfn.Condition.number_less_than_json_path('$.report.summary.passed', '$.report.summary.num_tests'),
            parse_report_job.next(send_notification_job).next(job_succeeded)
        )
        is_sent_notification.otherwise(job_succeeded)

        definition = sfn.Chain.start(test_website_job).next(generate_report_job).next(is_sent_notification)

        job_machine_name = '-'.join([construct_id, 'state machine'.replace(' ', '-')])
        job_machine = sfn.StateMachine(self, 'JobMachine',
                                       definition=definition,
                                       state_machine_name=job_machine_name,
                                       timeout=cdk.Duration.minutes(20))

        scheduler_event_name = '-'.join([construct_id, 'rule'.replace(' ', '-')])
        scheduler_event = events.Rule(
            self, "ScheduleRule",
            description='To trigger the testing for website',
            rule_name=scheduler_event_name,
            schedule=events.Schedule.expression('cron(*/10 * * * ? *)'),
            targets=[
                targets.SfnStateMachine(
                    job_machine
                )
            ]
        )

        cdk.Tags.of(job_machine).add('Name', job_machine_name.lower(), priority=50)
