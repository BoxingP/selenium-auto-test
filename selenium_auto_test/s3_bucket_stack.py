from aws_cdk import (
    aws_s3 as s3,
    core as cdk
)


class S3BucketStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        allure_results_bucket = s3.Bucket(self, 'AllureResults',
                                          bucket_name='-'.join([construct_id, 's3']), versioned=True,
                                          removal_policy=cdk.RemovalPolicy.DESTROY, auto_delete_objects=False,
                                          block_public_access=s3.BlockPublicAccess.BLOCK_ALL)
        self.lifecycle_rules(allure_results_bucket, expiration=365, noncurrent_expiration=14)
        self.allure_results_bucket = allure_results_bucket

    @staticmethod
    def lifecycle_rules(bucket, incomplete=7, is_transition=True, to_glacier=30, expiration=60,
                        noncurrent_expiration=60):
        bucket.add_lifecycle_rule(
            id="abort-incomplete-multipart-upload",
            abort_incomplete_multipart_upload_after=cdk.Duration.days(incomplete),
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
                noncurrent_version_transitions=[
                    s3.NoncurrentVersionTransition(
                        storage_class=s3.StorageClass.GLACIER,
                        transition_after=cdk.Duration.days(to_glacier)
                    )
                ],
                enabled=True
            )
        bucket.add_lifecycle_rule(
            id="expiration",
            expiration=cdk.Duration.days(expiration),
            enabled=True
        )
        bucket.add_lifecycle_rule(
            id="noncurrent-version-expiration",
            noncurrent_version_expiration=cdk.Duration.days(noncurrent_expiration),
            enabled=True
        )
