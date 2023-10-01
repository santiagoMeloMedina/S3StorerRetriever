import dotenv
import boto3
import pydantic
import pydantic_settings

from typing import Optional


dotenv.load_dotenv()


class AWSEnvironment(pydantic_settings.BaseSettings):
    aws_access_key_id: Optional[str] = ""
    aws_secret_access_key: Optional[str] = ""
    aws_session_token: Optional[str] = ""


class RoleConfiguration(pydantic_settings.BaseSettings):
    s3_access_role_arn: str
    s3_access_role_name: str
    s3_access_role_duration: int
    s3_bucket_name: str


CREDENTIALS_KEY = "Credentials"


class Credentials(pydantic.BaseModel):
    AccessKeyId: str
    SecretAccessKey: str
    SessionToken: str

    def export_format(self):
        return (
            "export AWS_ACCESS_KEY_ID=%s; export AWS_SECRET_ACCESS_KEY=%s; export AWS_SESSION_TOKEN=%s"
            % (self.AccessKeyId, self.SecretAccessKey, self.SessionToken)
        )


ROLE_CONFIG = RoleConfiguration()
AWS_ENVIRON = AWSEnvironment()


def get_credentials():
    sts_client = boto3.client("sts")

    response: dict = sts_client.assume_role(
        RoleArn=ROLE_CONFIG.s3_access_role_arn,
        RoleSessionName=ROLE_CONFIG.s3_access_role_name,
        DurationSeconds=ROLE_CONFIG.s3_access_role_duration,
    )

    creds = Credentials.model_validate(response.get(CREDENTIALS_KEY))

    if input("Exportable Creds? y|n: ").lower() == "y":
        print(creds.export_format())

    return creds


def with_creds(function):
    def wrapper():
        creds = None

        if input("Get Creds? y|n: ").lower() == "y":
            creds = get_credentials()
            print(creds)

        function(creds)

    return wrapper
