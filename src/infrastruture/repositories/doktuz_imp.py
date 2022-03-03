from pandas import DataFrame
from config import Logger
from src.infrastruture.external.connection import Connection
from src.infrastruture.repositories.doktuz import DoktuzRepository
from src.infrastruture.external.models import DoktuzDB 

class DoktuzRepositoryImp(DoktuzRepository):
    def __init__(self, connection: Connection):
         super().__init__(connection)

    def save_data(self, data:dict):
        try:
            doktuz = DoktuzDB(**data)
            session = self._connection.session()
            session.merge(doktuz, load=True)
            session.commit()
        except Exception as e:
            Logger.critical('DoktuzRepositoryImp.save_data: ', exc_info=True)
            session.rollback()
            raise e
        finally:
            if session is not None:
                session.close()
    
    def check_code(self, user_code:str):
        session = None
        try:
            session = self._connection.session()
            item = session.query(DoktuzDB).get(user_code)
            return item
        except Exception as e:
            Logger.warning('DoktuzRepositoryImp.check_code: ', exc_info=True)
            raise e
        finally:
            if session is not None:
                session.close()

    def save_excel_data(self, data:DataFrame):
        try:
            data.to_sql(name='base_vigilancia_medica', con=self._connection.engine, 
            if_exists='append', index=False)
        except Exception as e:
            Logger.critical('DoktuzRepositoryImp.save_excel_data:{0}'.format(e), exc_info=True)
            raise e