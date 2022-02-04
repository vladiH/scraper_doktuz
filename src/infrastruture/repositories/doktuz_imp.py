from src.infrastruture.external.factory_db import FactoryDataBase
from src.infrastruture.repositories.doktuz import DoktuzRepository
from src.infrastruture.external.models import DoktuzDB 

class DoktuzRepositoryImp(DoktuzRepository):
    def __init__(self, factoryDataBase: FactoryDataBase):
         super().__init__(factoryDataBase)

    def save_data(self, data:dict):
        try:
            doktuz = DoktuzDB(**data)
            session = self._factoryDataBase.session()
            session.add(doktuz)
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception("Could not save data")
    
    def there_is_code(self, user_code:str):
        try:
            session = self._factoryDataBase.session()
            return session.query(DoktuzDB).get(user_code)!=None
        except Exception as e:
            return False