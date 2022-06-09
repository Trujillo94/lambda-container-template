import logging

from src.wrappers.db.exception import DBException
from src.wrappers.db.connect import db_connection

logger = logging.getLogger("wrappers.db.controllers")


"""
Logic from Classes declared in entities.
This file is the bridge between the code and RDS
"""

@DBException.error_handling
def sample_function():
    db_session = db_connection.start_session()

    random_check = True

    if not random_check:
        raise DBException("DB is on fire!")

    db_session.commit()

    db_connection.close_session()
