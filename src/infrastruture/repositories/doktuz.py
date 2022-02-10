from abc import ABC, abstractmethod

from src.infrastruture.external.connection import Connection


class DoktuzRepository(ABC):
    def __init__(self,connection:Connection):
        self._connection = connection
    
    @abstractmethod
    def save_data(self, data:dict):
        pass

    @abstractmethod
    def there_is_code(self, user_code:str):
        pass