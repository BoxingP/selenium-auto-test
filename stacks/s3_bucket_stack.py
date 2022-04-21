from aws_cdk import (
    aws_iam as iam,
    aws_s3 as s3,
    core as cdk
)


class S3BucketStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, bucket_name: str, is_versioned: bool, public_dir: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3_bucket = s3.Bucket(
            self, 'S3Bucket',
            auto_delete_objects=False,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                ignore_public_acls=True,
                block_public_policy=False,
                restrict_public_buckets=False
            ),
            bucket_name=bucket_name,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            versioned=is_versioned
        )
        self.lifecycle_rules(
            s3_bucket, incomplete=7, is_versioned=is_versioned
        )
        s3_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=['s3:GetObject'],
                resources=[
                    f'arn:aws-cn:s3:::{bucket_name}/{public_dir}/*'
                ],
                sid='AllowPublicAccessForSpecificFolder'
            )
        )

        cdk.Tags.of(s3_bucket).add('Name', bucket_name.lower(), priority=50)

        cdk.CfnOutput(self, 'OutputS3BucketName',
                      export_name=construct_id.title().replace('-', '') + 'BucketName',
                      value=s3_bucket.bucket_name)

    @staticmethod
    def lifecycle_rules(bucket, incomplete: int, is_versioned: bool, is_expired=False, expiration=60,
                        is_transition=False, noncurrent_expiration=60, to_glacier=30):
        bucket.add_lifecycle_rule(
            id="abort-incomplete-multipart-upload",
            abort_incomplete_multipart_upload_after=cdk.Duration.days(incomplete),
            enabled=True
        )
        if is_expired:
            bucket.add_lifecycle_rule(
                id="expiration",
                expiration=cdk.Duration.days(expiration),
                enabled=True
            )
        if is_transition:
            bucket.add_lifecycle_rule(
                id="transitions-to-glacier",
                transitions=[
                    s3.Transition(
                        storage_class=s3.StorageClass.GLACIER,
                        transition_after=cdk.Duration.days(to_glacier)
                    )
                ],
                enabled=True
            )
        if is_versioned:
            bucket.add_lifecycle_rule(
                id="noncurrent-version-expiration",
                noncurrent_version_expiration=cdk.Duration.days(noncurrent_expiration),
                enabled=True
            )
            if is_transition:
                bucket.add_lifecycle_rule(
                    id="noncurrent-version-transitions-to-glacier",
                    noncurrent_version_transitions=[
                        s3.NoncurrentVersionTransition(
                            storage_class=s3.StorageClass.GLACIER,
                            transition_after=cdk.Duration.days(to_glacier)
                        )
                    ],
                    enabled=True
                )
