from src.infrastruture.external.postgresql import PostgresConnection
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
            host = crawler.settings.get('HOST'),
            data_base = crawler.settings.get('DATA_BASE'),
            user = crawler.settings.get('USER'),
            password = crawler.settings.get('PASSWORD'),
            port = crawler.settings.get('PORT')
        )
    def open_spider(self, spider):
        self.db = PostgresConnection(self.host, self.data_base, self.user, self.password, self.port)
        if self.db.connect():
            print("Connected to database")
        else:
            print("Could not connect to database")
        self.repository = DoktuzRepositoryImp(self.db)

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        self.repository.save_data(item)

    def is_recorded(self):
        pass