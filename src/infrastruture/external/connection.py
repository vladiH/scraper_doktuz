import sqlalchemy
from config import Logger
from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastruture.external.base import Base
class Connection(ABC):
    instance = None # Singleton instance
    def __init__(self, host, data_base, user, password, port):
        self.host = host
        self.data_base = data_base
        self.user = user
        self.password = password
        self.port = port
        self.engine = None

    @abstractmethod
    def connect(self)->bool:
        pass
    
    def init_engine(self, url):
        try:
            self.engine = create_engine(url, pool_size = 20)
            self.session:sessionmaker = sessionmaker(bind=self.engine)
            Base.metadata.create_all(self.engine, checkfirst=True)
        except Exception as e:
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.engine is not None:
            self.engine.dispose()
            self.engine = None
    
    def close(self):
        if self.engine is not None:
            self.engine.dispose()

    def execute(self, query):
        try:
            self.engine.execute(query)
        except sqlalchemy.exc.ProgrammingError as e:
            Logger.critical("Could not execute query: {}".format(e), exc_info=True)
            raise sqlalchemy.exc.SQLAlchemyError(e)