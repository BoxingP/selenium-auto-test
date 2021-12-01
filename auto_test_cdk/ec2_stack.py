import os

from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    core as cdk
)

OFFICE_IP = ['222.126.242.202', '222.126.242.203']


class EC2Stack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, vpc: ec2.Vpc, keypair_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        s3_bucket_name = cdk.Fn.import_value('AutoTestS3BucketName')

        amazon_linux_image = ec2.MachineImage.generic_linux(
            ami_map={os.getenv('AWS_DEFAULT_REGION'): 'ami-0f8d4b3ca40ae0bc6'})
        security_group = ec2.SecurityGroup(
            self, 'AllureSecurityGroup', vpc=vpc,
            description='Security group for allure server',
            security_group_name='-'.join([construct_id, 'allure sg'.replace(' ', '-')])
        )
        reading_s3_policy = iam.ManagedPolicy(
            self, 'ReadingS3Policy',
            managed_policy_name='-'.join(
                [construct_id, 'reading s3 policy'.replace(' ', '-')]
            ),
            description='Policy to read S3 bucket',
            statements=[
                iam.PolicyStatement(
                    sid='AllowListOfSpecificBucket',
                    actions=['s3:ListBucket'],
                    resources=[
                        'arn:aws-cn:s3:::' + s3_bucket_name,
                        'arn:aws-cn:s3:::' + s3_bucket_name + '/*'
                    ]
                ),
                iam.PolicyStatement(
                    sid='AllowGetObjectOfSpecificBucket',
                    actions=['s3:GetObject'],
                    resources=[
                        'arn:aws-cn:s3:::' + s3_bucket_name,
                        'arn:aws-cn:s3:::' + s3_bucket_name + '/*'
                    ]
                )
            ]
        )
        allure_role = iam.Role(
            self, 'AllureRole',
            assumed_by=iam.ServicePrincipal('ec2.amazonaws.com.cn'),
            description="IAM role for allure server",
            managed_policies=[reading_s3_policy],
            role_name='-'.join([construct_id, 'allure server role'.replace(' ', '-')]),
        )
        allure_instance = ec2.Instance(
            self, 'AllureEC2',
            instance_type=ec2.InstanceType('t2.micro'),
            machine_image=amazon_linux_image,
            vpc=vpc,
            block_devices=[
                ec2.BlockDevice(
                    device_name='/dev/xvda',
                    volume=ec2.BlockDeviceVolume.ebs(
                        volume_size=8,
                        encrypted=False,
                        delete_on_termination=True,
                        volume_type=ec2.EbsDeviceVolumeType.GP2
                    )
                )
            ],
            instance_name='-'.join([construct_id, 'allure'.replace(' ', '-')]),
            key_name=keypair_name,
            role=allure_role,
            security_group=security_group,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
        )
        for ip in OFFICE_IP:
            security_group.add_ingress_rule(
                peer=ec2.Peer.ipv4(ip + '/32'),
                connection=ec2.Port(
                    protocol=ec2.Protocol.TCP,
                    string_representation="tcp on all ports",
                    from_port=0,
                    to_port=65535),
                description='from office')

        cdk.CfnOutput(self, 'OutputAllureInstanceId',
                      export_name='AllureInstanceId', value=allure_instance.instance_id)
        cdk.CfnOutput(self, 'OutputAllurePublicIP',
                      export_name='AllureInstancePublicIP', value=allure_instance.instance_public_ip)
        cdk.CfnOutput(self, 'OutputAllureInstanceKeypair',
                      export_name='AllureInstanceKeypairName', value=keypair_name)
