import logging

from src.config.dynamodb import DYNAMODB_ENDPOINT_URL
from src.wrappers.aws.connect import boto3_session
from src.wrappers.aws.exception import AWSException

logger = logging.getLogger("wrappers.aws.dynamodb")


class DynamoDBWrapper:

    @AWSException.error_handling
    def __init__(self):
        """
        Creates the DynamoDB boto3 resource with the DB URL set in the config
        """
        self.__session = boto3_session
        self.__dynamodb = self.__session.resource("dynamodb", endpoint_url=DYNAMODB_ENDPOINT_URL)

    @AWSException.error_handling
    def create_item(self, table_name, item_data):
        """
        Creates a new item with the given data in the desired table.

        :param table_name: String with the table name
        :param item_data: dictionary with the new item data
        returns: The new item as a dict
        """

        logger.info(f"Creating item in '{table_name}': '{item_data}'")

        table = self.__dynamodb.table(table_name)
        response = table.put_item(Item=item_data)
        logger.debug(f"Boto3 response: '{response}'")

        return response["Item"]

    @AWSException.error_handling
    def get_item(self, table_name, item_key):
        """
        Get an item with the given data in the desired table.

        :param table_name: String with the table name
        :param item_key: Key to identify the item
        returns: The item as a dict
        """

        logger.info(f"Getting item '{table_name}'-'{item_key}'")

        table = self.__dynamodb.table(table_name)
        response = table.get_item(Key=item_key)
        logger.debug(f"Boto3 response: '{response}'")

        return response["Item"]

    @AWSException.error_handling
    def update_item(self, table_name, item_key, attributes):
        """
        Get an item with the given data in the desired table.

        :param table_name: String with the table name
        :param item_key: Key to identify the item
        :param attributes: Dict with the attributes to change
        returns: The item with the modified data
        """

        logger.info(f"Updating item '{table_name}'-'{item_key}' attributes: '{attributes}'")

        # Build the UpdateExpression string, more info in:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
        # UpdateExpression string format: 'SET #<attribute_name> = :<attribute_name>_value'
        update_expression = "SET {}".format(",".join(f"#{attribute} = :{attribute}_value" for attribute in attributes))

        # <value_name> definitions
        # Dict with key = ':<attribute_name>_value' and value = '<attribute_value>'
        expression_attribute_values = {f":{attribute}_value": value for attribute, value in attributes.items()}

        table = self.__dynamodb.Table(table_name)
        response = table.update_item(
            Key=item_key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW",
        )
        logger.debug(f"Boto3 response: '{response}'")

        return response
