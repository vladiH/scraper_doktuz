from datetime import datetime
from config import Config, Logger
from src.infrastruture.external.factory_connection import FactoryConnection
from src.infrastruture.repositories.doktuz_imp import *
class DatabasePipeline:
    def __init__(self,host, data_base, user, password, port, db_type):
        self.host = host
        self.data_base = data_base
        self.user = user
        self.password = password
        self.port = port
        self.db_type = db_type

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host = Config.HOST,
            data_base = Config.DATA_BASE,
            user = Config.USER,
            password = Config.PASSWORD,
            port = Config.PORT,
            db_type = Config.DB_TYPE
        )
    def open_spider(self, spider):
        try:
            self.db = FactoryConnection.get_connection(self.host, self.data_base, self.user, self.password, self.port, self.db_type)
            Logger.info("DatabasePipeline: Connected to database")
            self.repository = DoktuzRepositoryImp(self.db)
        except Exception as e:
            Logger.critical('DatabasePipeline.open_spider: ', exc_info=True)
            raise e

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        print('Item {}, hora: {}'.format(item, datetime.now()))
        if item!=None:
            self.repository.save_data(item)