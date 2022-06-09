import logging

from src.utils.exception import GenericException, error_handling
from src.wrappers.db.connect import db_connection

logger = logging.getLogger("wrappers.db.exception")


class DBException(GenericException):

    @classmethod
    @error_handling
    def error_handling(cls, function):
        """
        Expands error_handling in utils/exception.py to ensure the DB session is always closes
        even if an exception occurs.
        """
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            finally:
                # Ensure DB session is closed
                try:
                    db_connection.close_session()
                except Exception as e:
                    msg = f"'{function.__name__}' - Unexpected error closing DB session: '{e}'"
                    logger.error(msg)
                    raise DBException(msg)

        wrapper.__name__ = function.__name__
        return wrapper
