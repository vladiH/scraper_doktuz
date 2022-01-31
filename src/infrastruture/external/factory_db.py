from abc import ABC, abstractmethod

from sqlalchemy import engine
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

    @abstractmethod
    def execute(self, query):
        pass