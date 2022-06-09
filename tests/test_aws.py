from src.wrappers.aws.connect import boto3_session
from src.wrappers.aws.s3 import S3Wrapper
from src.wrappers.aws.dynamodb import DynamoDBWrapper


def test_boto3_session():
    boto3_session.get_available_services()


def test_s3_connection():
    s3 = S3Wrapper()
    s3.list_buckets()


def test_dynamodb_connection():
    DynamoDBWrapper()
