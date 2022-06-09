import logging
import traceback

from botocore.exceptions import ClientError

from src.utils.exception import GenericException, error_handling

logger = logging.getLogger("wrappers.aws.exception")


class AWSException(GenericException):

    @classmethod
    @error_handling
    def error_handling(cls, function):
        """
        Expands the error_handing found in utils/exception.py to handle ClientError
        and log them as an error with the Boto3 session.
        """

        def wrapper(*args, **kwargs):

            try:
                return function(*args, **kwargs)
            except ClientError as e:
                msg = f"'{function.__name__}' - Boto3 error: '{e}'"
                stack_trace = traceback.format_exc()
                logger.error(f"{msg} - Stack trace: '{stack_trace}'")
                raise AWSException(msg, original_exception=e)

        wrapper.__name__ = function.__name__
        return wrapper
