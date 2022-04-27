from aws_cdk import (
    aws_events as events,
    aws_iam as iam,
    aws_events_targets as targets,
    aws_lambda as _lambda,
    aws_sns as sns,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfn_tasks,
    core as cdk
)


class StepFunctionsStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, schedule: str, subject: str, **kwargs) -> None:
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
            subject=subject,
            input_path='$.notification',
            result_path='$'
        )

        job_succeeded_job = sfn.Succeed(self, 'JobIsSucceeded')

        is_sent_notification_job = sfn.Choice(self, 'DecideWhetherSendNotification', output_path='$')
        is_sent_notification_job.when(
            sfn.Condition.number_less_than_json_path('$.report.summary.passed', '$.report.summary.num_tests'),
            parse_report_job.next(send_notification_job).next(job_succeeded_job)
        )
        is_sent_notification_job.otherwise(job_succeeded_job)

        definition = sfn.Chain.start(test_website_job).next(generate_report_job).next(is_sent_notification_job)

        state_machine_role_name = '-'.join([construct_id, 'state machine role'.replace(' ', '-')])
        state_machine_role = iam.Role(
            self, 'StateMachineRole',
            assumed_by=iam.ServicePrincipal('states.amazonaws.com'),
            description="IAM role for testing website's state machine",
            managed_policies=[],
            role_name=state_machine_role_name,
        )
        state_machine_name = '-'.join([construct_id, 'state machine'.replace(' ', '-')])
        state_machine = sfn.StateMachine(
            self, 'StateMachine',
            definition=definition,
            role=state_machine_role,
            state_machine_name=state_machine_name,
            timeout=cdk.Duration.minutes(20)
        )

        event_rule_role_name = '-'.join([construct_id, 'event rule role'.replace(' ', '-')])
        event_rule_role = iam.Role(
            self, 'EventRuleRole',
            assumed_by=iam.ServicePrincipal('events.amazonaws.com'),
            description='IAM role for event rule which triggers testing website',
            managed_policies=[],
            role_name=event_rule_role_name,
        )
        event_rule_name = '-'.join([construct_id, 'rule'.replace(' ', '-')])
        event_rule = events.Rule(
            self, "EventRule",
            description='To trigger the testing for website',
            enabled=True,
            rule_name=event_rule_name,
            schedule=events.Schedule.expression(schedule),
            targets=[
                targets.SfnStateMachine(
                    state_machine, role=event_rule_role
                )
            ]
        )

        cdk.Tags.of(state_machine_role).add('Name', state_machine_role_name.lower(), priority=50)
        cdk.Tags.of(state_machine).add('Name', state_machine_name.lower(), priority=50)
        cdk.Tags.of(event_rule_role).add('Name', event_rule_role_name.lower(), priority=50)
