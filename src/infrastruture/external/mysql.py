
from config import Logger
from src.infrastruture.external.connection import Connection
class MysqlConnection(Connection):
    
    def __init__(self, host, data_base, user, password, port):
        """
        Get SQLalchemy engine using credentials.
        Input:
        db: database name
        user: Username
        host: Hostname of the database server
        port: Port number
        passwd: Password for the database
        """
        super().__init__(host, data_base, user, password, port)
        self.connect()
        

    @classmethod
    def getInstance(cls,host, data_base, user, password, port):
        if not cls.instance:
            cls.instance = MysqlConnection(host, data_base, user, password, port)
        return cls.instance

    def connect(self):
        try:
            url = 'mysql://{user}:{passwd}@{host}:{port}/{db}'.format(
            user=self.user, passwd=self.password, host=self.host, port=self.port, db=self.data_base)
            self.init_engine(url)
        except Exception as e:
            Logger.critical("Could not connect to database", exc_info=True)
            raise e