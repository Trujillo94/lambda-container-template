import logging

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from src.config.rds import SQL, USERNAME, PASSWORD, HOST, DATABASE
from src.wrappers.db.exception import DBException

logger = logging.getLogger("wrappers.db.connect")


class DBConnection:

    @DBException.error_handling
    def __init__(self):
        """
        Initializes a SQL engine connected to the DB
        and a SQLAlchemy Session Maker using this engine.
        """
        self.session = None
        self.__url = f"{SQL}://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"

        self.__engine = self.__create_db_engine()
        self.__session_maker = self.__initialize_session_maker()
        self.metadata = self.__retrieve_db_metadata()

    @DBException.error_handling
    def __create_db_engine(self):
        """
        Creates a DB engine connected to the url set in the attributes.

        :return: The DB engine
        """
        url = self.__url

        try:
            engine = create_engine(url, echo=False)
            return engine
        except Exception as e:
            logger.error(f"Unexpected error creating DB engine: '{e}'")
            raise e

    @DBException.error_handling
    def __initialize_session_maker(self):
        """
        Initializes a SQLAlchemy Session Maker using the engine stored in the attributes.

        :return: The Session Maker
        """
        engine = self.__engine

        session_maker = sessionmaker()
        session_maker.configure(bind=engine)
        return session_maker

    @DBException.error_handling
    def __retrieve_db_metadata(self):
        """
        Retrieves all the DB MetaData from the engine set in the attributes.

        :return: The DB metadata
        """
        engine = self.__engine

        metadata = MetaData(bind=engine)
        metadata.reflect()
        return metadata

    @DBException.error_handling
    def start_session(self):
        """
        Starts a DB session using the Session Maker in the attributes.
        If a session has already been started, return it instead so only
        one session can be used per instance.

        :return: The session that has been created
        """

        session_maker = self.__session_maker()

        if self.session is None:
            session = session_maker()
            self.session = session
        else:
            session = self.session
        return session

    @DBException.error_handling
    def close_session(self):
        """
        Closes the session if it has been started.
        """

        session = self.session

        if session is not None:
            session.close()
            self.session = None


db_connection = DBConnection()
