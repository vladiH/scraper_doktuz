from config import Config, Logger
from src.infrastruture.external.factory_connection import FactoryConnection
from src.infrastruture.repositories.doktuz_imp import *
class CheckDataBasePipeline:
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
        store_item = self.repository.check_code(item['codigo'])
        if store_item != None:
            flag = None
            if not store_item.certificado_downloaded and store_item.certificado!=None:
                #item['codigo'] = store_item.codigo
                #item['fecha'] = store_item.fecha
                #item['empresa'] = store_item.empresa
                #item['subcontrata'] = store_item.subcontrata
                #item['proyecto'] = store_item.proyecto
                #item['t_exam'] = store_item.t_exam
                #item['paciente'] = store_item.paciente
                item['certificado'] = store_item.certificado
                item['certificado_downloaded'] = store_item.certificado_downloaded
                flag = True
                
            if not store_item.imp_downloaded and store_item.imp!=None:
                item['imp_downloaded'] = store_item.imp_downloaded
                item['imp'] = store_item.imp
                flag = True
            if flag!=None:
                return item
        else:
            return item