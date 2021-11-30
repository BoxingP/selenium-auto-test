from aws_cdk import (
    aws_events as events,
    aws_events_targets as targets,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfn_tasks,
    core as cdk
)


class SchedulerStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, lambda_functions: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        test_website_job = sfn_tasks.LambdaInvoke(
            self, 'TestWebsite',
            lambda_function=lambda_functions.get('test_website'),
            timeout=cdk.Duration.minutes(5)
        )

        generate_report_job = sfn_tasks.LambdaInvoke(
            self, 'GenerateReport',
            lambda_function=lambda_functions.get('generate_report'),
            timeout=cdk.Duration.minutes(5)
        )

        job_succeeded = sfn.Succeed(self, 'JobIsSucceeded')

        definition = sfn.Chain.start(test_website_job).next(generate_report_job).next(job_succeeded)

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
