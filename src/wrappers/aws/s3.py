import logging

from src.wrappers.aws.connect import boto3_session
from src.wrappers.aws.exception import AWSException

logger = logging.getLogger("wrappers.aws.s3")


class S3Wrapper:

    @AWSException.error_handling
    def __init__(self):
        self.__s3_client = boto3_session.client("s3")

    @AWSException.error_handling
    def list_buckets(self):
        """
        List all the buckets in the selected region.

        return: List with all the buckets
        """
        s3_buckets = self.__s3_client.list_buckets()
        return s3_buckets["Buckets"]

    @AWSException.error_handling
    def get_object_data(self, bucket, key):
        """
        Get the content of an S3 object.

        :param bucket: S3 bucket where the file is located
        :param key: S3 prefix of the file
        :return: botocore.response.StreamingBody object of the file
        """
        s3_client = self.__s3_client

        logger.info(f"Getting S3 object - Bucket: '{bucket}' - Key: '{key}'")
        s3_object = s3_client.get_object(Bucket=bucket, Key=key)
        logger.debug(f"Boto3 response: '{s3_object}'")

        return s3_object["Body"]

    @AWSException.error_handling
    def upload_file(self, bucket, local_file_name, s3_file_name=None):
        """
        Uploads a file into S3 to the selected bucket.

        :param bucket: String with the name of the S3 bucket
        :param local_file_name: String with local file path
        :param s3_file_name: String with the path in the s3 bucket where the file will be uploaded
        return: Boto3 response
        """

        s3_client = self.__s3_client.client("s3")
        response = s3_client.upload_file(local_file_name, bucket, s3_file_name)
        return response

    @AWSException.error_handling
    def list_bucket_objects(self, bucket):
        """
        Lists all objects within a bucket, with a maximum of 1000 objects returned per call.

        :param bucket: String with the bucket name
        return: List with the bucket contents
        """

        contents = []
        for item in self.__s3_client.list_objects_v2(Bucket=bucket)["Contents"]:
            contents.append(item)
        return contents
