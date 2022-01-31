from infrastruture.external.factory_db import FactoryDataBase
from infrastruture.repositories.doktuz import DoktuzRepository


class DoktuzRepositoryImp(DoktuzRepository):
    def __init__(self, factoryDataBase: FactoryDataBase):
         super().__init__(factoryDataBase)

    def save(self, data:dict):
        query = "insert into doktuz ({keyTuple}) values {valTuple}".format(keyTuple=",\n ".join(data), valTuple=tuple(data.values()))
        self.factoryDataBase.execute(query)