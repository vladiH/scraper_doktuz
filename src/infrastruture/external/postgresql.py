
import sqlalchemy
import logging
from src.infrastruture.external.factory_db import FactoryDataBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
logger = logging.getLogger(__name__)
class PostgresConnection(FactoryDataBase):
    def __init__(self, host, data_base, user, password, port):
        """
        Get SQLalchemy engine using credentials.
        Input:
        db: database name
        user: Username
        host: Hostname of the database server
        port: Port number
        passwd: Password for the database
        """
        super().__init__(host, data_base, user, password, port)
        

    def connect(self):
        try:
            url = 'postgresql://{user}:{passwd}@{host}:{port}/{db}'.format(
            user=self.user, passwd=self.password, host=self.host, port=self.port, db=self.data_base)
            self.init_engine(url)
            return True
        except sqlalchemy.exc.OperationalError:
            logger.critical("Could not connect to database", exc_info=True)
            return False

    def execute(self, query):
        try:
            self.engine.execute(query)
        except sqlalchemy.exc.ProgrammingError as e:
            logger.critical("Could not execute query: {}".format(e), exc_info=True)
            raise sqlalchemy.exc.SQLAlchemyError(e)