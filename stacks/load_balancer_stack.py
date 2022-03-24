from aws_cdk import (
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_iam as iam,
    core as cdk
)


class LoadBalancerStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str,
                 ami: str, vpc: ec2.Vpc, bucket_name: str, keypair_name: str, ec2_inbounds: list,
                 loadbalancer_inbounds: list, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        reading_s3_policy_name = '-'.join([construct_id, 'reading s3'.replace(' ', '-')])
        reading_s3_policy = iam.ManagedPolicy(
            self, 'ReadingS3Policy',
            managed_policy_name=reading_s3_policy_name,
            description='Policy to read S3 bucket',
            statements=[
                iam.PolicyStatement(
                    sid='AllowListOfSpecificBucket',
                    actions=['s3:ListBucket'],
                    resources=[
                        'arn:aws-cn:s3:::' + bucket_name,
                        'arn:aws-cn:s3:::' + bucket_name + '/*'
                    ]
                ),
                iam.PolicyStatement(
                    sid='AllowGetObjectOfSpecificBucket',
                    actions=['s3:GetObject'],
                    resources=[
                        'arn:aws-cn:s3:::' + bucket_name,
                        'arn:aws-cn:s3:::' + bucket_name + '/*'
                    ]
                )
            ]
        )
        iam_role_name = '-'.join([construct_id, 'server role'.replace(' ', '-')])
        iam_role = iam.Role(
            self, 'IAMRole',
            assumed_by=iam.ServicePrincipal('ec2.amazonaws.com.cn'),
            description="IAM role for allure report server",
            managed_policies=[reading_s3_policy],
            role_name=iam_role_name
        )

        ec2_security_group_name = '-'.join([construct_id, 'server sg'.replace(' ', '-')])
        ec2_security_group = ec2.SecurityGroup(
            self, 'EC2SecurityGroup', vpc=vpc,
            description='Security group for allure report server',
            security_group_name=ec2_security_group_name
        )
        for inbound in ec2_inbounds:
            for port in inbound['port']:
                if '-' in str(port):
                    [from_port, to_port] = str(port).split('-')
                else:
                    from_port = port
                    to_port = port
                ec2_security_group.add_ingress_rule(
                    peer=ec2.Peer.ipv4(inbound['ip']),
                    connection=ec2.Port(
                        protocol=ec2.Protocol.TCP,
                        string_representation=inbound['description'],
                        from_port=int(from_port),
                        to_port=int(to_port)
                    ),
                    description=inbound['description']
                )

        auto_scaling_group = autoscaling.AutoScalingGroup(
            self, 'AutoScalingGroup',
            instance_type=ec2.InstanceType('t2.medium'),
            machine_image=ec2.MachineImage.generic_linux(ami_map={self.region: ami}),
            vpc=vpc,
            role=iam_role,
            security_group=ec2_security_group,
            allow_all_outbound=True,
            associate_public_ip_address=False,
            auto_scaling_group_name='-'.join([construct_id, 'asg']),
            block_devices=[
                autoscaling.BlockDevice(
                    device_name='/dev/xvda',
                    volume=autoscaling.BlockDeviceVolume.ebs(
                        volume_size=8,
                        encrypted=False,
                        delete_on_termination=True,
                        volume_type=autoscaling.EbsDeviceVolumeType.GP2
                    )
                )
            ],
            desired_capacity=1,
            key_name=keypair_name,
            max_capacity=1,
            min_capacity=1,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE)
        )
        auto_scaling_group.apply_removal_policy(cdk.RemovalPolicy.DESTROY)

        loadbalancer_security_group_name = '-'.join([construct_id, 'load sg'.replace(' ', '-')])
        loadbalancer_security_group = ec2.SecurityGroup(
            self, 'LoadSecurityGroup', vpc=vpc,
            description='Security group for load balancer',
            security_group_name=loadbalancer_security_group_name
        )
        for inbound in loadbalancer_inbounds:
            for port in inbound['port']:
                if '-' in str(port):
                    [from_port, to_port] = str(port).split('-')
                else:
                    from_port = port
                    to_port = port
                loadbalancer_security_group.add_ingress_rule(
                    peer=ec2.Peer.ipv4(inbound['ip']),
                    connection=ec2.Port(
                        protocol=ec2.Protocol.TCP,
                        string_representation=inbound['description'],
                        from_port=int(from_port),
                        to_port=int(to_port)
                    ),
                    description=inbound['description']
                )
        load_balancer_name = '-'.join([construct_id, 'app'])
        load_balancer = elbv2.ApplicationLoadBalancer(
            self, 'LoadBalancer',
            security_group=loadbalancer_security_group,
            vpc=vpc,
            internet_facing=True,
            load_balancer_name=load_balancer_name
        )
        load_balancer.apply_removal_policy(cdk.RemovalPolicy.DESTROY)
        target_group_name = '-'.join([construct_id, 'tg'])
        target_group = elbv2.ApplicationTargetGroup(
            self, 'TargetGroup',
            port=80,
            protocol=elbv2.ApplicationProtocol.HTTP,
            targets=[auto_scaling_group],
            target_group_name=target_group_name,
            vpc=vpc
        )
        listener = elbv2.ApplicationListener(
            self, 'AppListener',
            load_balancer=load_balancer,
            open=False,
            protocol=elbv2.ApplicationProtocol.HTTP
        )
        listener.add_action(
            'AppListenerAction',
            action=elbv2.ListenerAction.forward(
                target_groups=[
                    target_group
                ]
            )
        )
        listener.apply_removal_policy(cdk.RemovalPolicy.DESTROY)

        cdk.Tags.of(iam_role).add('Name', iam_role_name.lower(), priority=50)
        cdk.Tags.of(ec2_security_group).add('Name', ec2_security_group_name.lower(), priority=50)
        cdk.Tags.of(loadbalancer_security_group).add('Name', loadbalancer_security_group_name.lower(), priority=50)
        cdk.Tags.of(load_balancer).add('Name', load_balancer_name.lower(), priority=50)
        cdk.Tags.of(target_group).add('Name', target_group_name.lower(), priority=50)

        cdk.CfnOutput(self, 'OutputLoadBalancerDnsName',
                      export_name=construct_id.title().replace('-', '') + 'DnsName',
                      value=load_balancer.load_balancer_dns_name)
        cdk.CfnOutput(self, 'OutputLoadBalancerEc2KeypairName',
                      export_name=construct_id.title().replace('-', '') + 'Ec2KeypairName',
                      value=keypair_name)
