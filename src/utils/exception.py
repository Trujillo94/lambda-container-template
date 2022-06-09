import logging
import traceback

logger = logging.getLogger("utils.exception")


class GenericException(Exception):
    """
    GenericException wraps Exception to provide an easier interface for exception handling
    to be used whenever we want to intentionally raise an exception from within our code.
    """

    def __init__(self, msg, original_exception=None):
        self.full_msg = f"{self.__class__.__name__}: '{msg}'"
        self.original_exception = original_exception

        if original_exception:
            self.full_msg += f" - Original exception: '{original_exception}'"

        super().__init__(self.full_msg)


def error_handling(function):
    """
    Decorator to be used as error handling on any function.
    Handles any child of Exception, logs it as an error, and raises it again as
    a GenericException.
    """

    def wrapper(*args, **kwargs):

        try:
            return function(*args, **kwargs)

        except GenericException as intentionally_raised:
            # If it is a GenericException, it was intentionally raised, so we re-raise it
            raise intentionally_raised
        except Exception as e:
            msg = f"'{function.__name__}' - Unexpected error: '{e}'"
            stack_trace = traceback.format_exc()
            logger.error(f"{msg} - Stack trace: '{stack_trace}'")
            raise GenericException(msg, original_exception=e)

    wrapper.__name__ = function.__name__
    return wrapper
