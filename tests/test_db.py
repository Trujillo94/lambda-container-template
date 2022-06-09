from src.wrappers.db.connect import db_connection


def test_db_connection():
    db_connection.start_session()
    db_connection.close_session()
