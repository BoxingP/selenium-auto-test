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
                function_arn=cdk.Fn.import_value('TestWebsiteLambdaArn')
            ),
            result_path='$',
            result_selector={
                'number_of_failed_tests.$': '$.Payload'
            },
            timeout=cdk.Duration.minutes(5)
        )

        generate_report_job = sfn_tasks.LambdaInvoke(
            self, 'GenerateReport',
            lambda_function=_lambda.Function.from_function_arn(
                self, 'GenerateReportLambda',
                function_arn=cdk.Fn.import_value('GenerateReportArn')
            ),
            result_path=sfn.JsonPath.DISCARD,
            timeout=cdk.Duration.minutes(5)
        )

        create_message_job = sfn_tasks.EvaluateExpression(
            self, "CreateMessage",
            expression="`Tests failed number: ${$.number_of_failed_tests}\nPlease check the details in the report.`",
            runtime=_lambda.Runtime.NODEJS_14_X,
            result_path="$.message"
        )

        send_notification_job = sfn_tasks.SnsPublish(
            self, 'SendNotification',
            topic=sns.Topic.from_topic_arn(
                self, 'SendNotificationTopic',
                topic_arn=cdk.Fn.import_value('SNSTopicArn')
            ),
            message=sfn.TaskInput.from_json_path_at("$.message"),
            subject='There Are Failed Tests Occurred on the Website',
            result_path="$.sns"
        )

        job_succeeded = sfn.Succeed(self, 'JobIsSucceeded')

        is_sent_notification = sfn.Choice(self, 'DecideWhetherSendNotification')
        is_sent_notification.when(sfn.Condition.number_greater_than('$.number_of_failed_tests', 0),
                                  create_message_job.next(send_notification_job).next(job_succeeded))
        is_sent_notification.otherwise(job_succeeded)

        definition = sfn.Chain.start(test_website_job).next(generate_report_job).next(is_sent_notification)

        job_machine = sfn.StateMachine(self, 'JobMachine',
                                       definition=definition,
                                       state_machine_name='-'.join([construct_id, 'state machine'.replace(' ', '-')]),
                                       timeout=cdk.Duration.minutes(20))

        scheduler_event = events.Rule(
            self, "ScheduleRule",
            description='To trigger the testing for website',
            rule_name='-'.join([construct_id, 'rule'.replace(' ', '-')]),
            schedule=events.Schedule.expression('cron(*/10 * * * ? *)'),
            targets=[
                targets.SfnStateMachine(
                    job_machine
                )
            ]
        )
