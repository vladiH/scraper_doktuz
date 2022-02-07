from src.infrastruture.external.models import DoktuzDB
from abc import ABC, abstractmethod
from sqlalchemy import engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastruture.external.base import Base
class FactoryDataBase(ABC):
    def __init__(self, host, data_base, user, password, port):
        self.host = host
        self.data_base = data_base
        self.user = user
        self.password = password
        self.port = port

    @abstractmethod
    def connect(self)->bool:
        pass
    
    def init_engine(self, url):
        try:
            self.engine = create_engine(url, pool_size = 5)
            self.session:sessionmaker = sessionmaker(bind=self.engine)
            Base.metadata.create_all(self.engine, checkfirst=True)
        except Exception as e:
            raise e

    @abstractmethod
    def execute(self, query):
        pass

    def close(self):
        self.engine.dispose()