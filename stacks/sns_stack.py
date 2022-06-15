from aws_cdk import (
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    core as cdk
)


class SNSStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        topic = config['topic']
        subscribers = config['subscribers']

        topic_name = '-'.join([construct_id, 'topic'.replace(' ', '-')])

        notification_topic = sns.Topic(
            self, 'SNSTopic',
            display_name=topic,
            topic_name=topic_name
        )
        for subscriber in subscribers:
            notification_topic.add_subscription(subscriptions.EmailSubscription(email_address=subscriber))
        notification_topic.apply_removal_policy(cdk.RemovalPolicy.DESTROY)

        cdk.Tags.of(notification_topic).add('Name', topic_name.lower(), priority=50)

        cdk.CfnOutput(self, 'OutputSnsTopicArn',
                      export_name=construct_id.title().replace('-', '') + 'TopicArn',
                      value=notification_topic.topic_arn)
