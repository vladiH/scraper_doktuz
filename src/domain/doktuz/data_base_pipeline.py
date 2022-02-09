from config import Config, Logger
from src.infrastruture.external.postgresql import PostgresConnection
from src.infrastruture.external.mysql import MysqlConnection
from src.infrastruture.repositories.doktuz_imp import *
class DatabasePipeline:
    def __init__(self,host, data_base, user, password, port):
        self.host = host
        self.data_base = data_base
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host = Config.HOST,
            data_base = Config.DATA_BASE,
            user = Config.USER,
            password = Config.PASSWORD,
            port = Config.PORT
        )
    def open_spider(self, spider):
        try:
            self.db = PostgresConnection(self.host, self.data_base, self.user, self.password, self.port)
            self.db.connect()
            Logger.info("DatabasePipeline: Connected to database")
            self.repository = DoktuzRepositoryImp(self.db)
        except Exception as e:
            Logger.critical('DatabasePipeline.open_spider: ', exc_info=True)
            raise e

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        self.repository.save_data(item)