from src.wrappers.db.connect import db_connection


tableA = db_connection.metadata.tables["table_name_A"]
tableB = db_connection.metadata.tables["table_name_B"]
