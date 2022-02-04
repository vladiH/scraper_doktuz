from abc import ABC, abstractmethod

from src.infrastruture.external.factory_db import FactoryDataBase


class DoktuzRepository(ABC):
    def __init__(self,factoryDataBase:FactoryDataBase):
        self._factoryDataBase = factoryDataBase
    
    @abstractmethod
    def save_data(self, data:dict):
        pass

    @abstractmethod
    def there_is_code(self, user_code:str):
        pass