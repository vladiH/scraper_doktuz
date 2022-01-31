from abc import ABC, abstractmethod

from infrastruture.external.factory_db import FactoryDataBase


class DoktuzRepository(ABC):
    def __init__(self,factoryDataBase:FactoryDataBase):
        self._factoryDataBase = factoryDataBase
    
    @abstractmethod
    def saveData(self, data:dict):
        pass