from src.config import \
    aws, \
    rds, \
    dynamodb


def test_aws_config():
    assert aws.SECRET_ACCESS_KEY is not None
    assert aws.ACCESS_KEY_ID is not None


def test_dynamodb_config():
    assert dynamodb.DYNAMODB_ENDPOINT_URL is not None


def test_rds_config():
    assert rds.SQL is not None
    assert rds.HOST is not None
    assert rds.PORT is not None
    assert rds.USERNAME is not None
    assert rds.PASSWORD is not None
    assert rds.DATABASE is not None
