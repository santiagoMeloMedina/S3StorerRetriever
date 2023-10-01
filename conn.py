import boto3

from session import AWS_ENVIRON, Credentials


class S3Files:
    def __init__(self, creds: Credentials = None):
        self.client = (
            boto3.client(
                "s3",
                aws_access_key_id=creds.AccessKeyId,
                aws_secret_access_key=creds.SecretAccessKey,
                aws_session_token=creds.SessionToken,
            )
            if creds
            else boto3.client("s3", **AWS_ENVIRON.model_dump())
        )
