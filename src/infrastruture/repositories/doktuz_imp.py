from pandas import DataFrame
from config import Logger
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
            Logger.critical('DoktuzRepositoryImp.save_data: ', exc_info=True)
            session.rollback()
            raise e
    
    def there_is_code(self, user_code:str):
        try:
            session = self._factoryDataBase.session()
            return session.query(DoktuzDB).get(user_code)!=None
        except Exception as e:
            Logger.warning('DoktuzRepositoryImp.there_is_code: ', exc_info=True)
            return False

    def save_excel_data(self, data:DataFrame):
        try:
            data.to_sql(name='base_vigilancia_medica', con=self._factoryDataBase.engine(), 
            if_exists='append', index=False)
        except Exception as e:
            Logger.critical('DoktuzRepositoryImp.save_excel_data: ', exc_info=True)
            raise e