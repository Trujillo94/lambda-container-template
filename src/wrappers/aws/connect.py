import boto3
import logging

from src.config.aws import ACCESS_KEY_ID, SECRET_ACCESS_KEY, SESSION_TOKEN, DEFAULT_REGION
from src.wrappers.aws.exception import AWSException

logger = logging.getLogger("wrappers.aws.connect")


@AWSException.error_handling
def initialize_boto3_session():
    """
    Initializes a boto3 session with the credentials found in AWS config variables.
    Only uses SESSION_TOKEN (for Lambda) or DEFAULT_REGION if they are set.

    :return: The boto3 session object
    """

    session_parameters = {
        "aws_access_key_id": ACCESS_KEY_ID,
        "aws_secret_access_key": SECRET_ACCESS_KEY
    }
    if SESSION_TOKEN is not None:
        session_parameters["aws_session_token"] = SESSION_TOKEN
    if DEFAULT_REGION is not None:
        session_parameters["region_name"] = DEFAULT_REGION

    session = boto3.Session(**session_parameters)

    return session

boto3_session = initialize_boto3_session()
