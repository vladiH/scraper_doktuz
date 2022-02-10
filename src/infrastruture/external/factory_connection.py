from config import Logger
from src.infrastruture.external.connection import Connection
from src.infrastruture.external.postgresql import PostgresConnection
from src.infrastruture.external.mysql import MysqlConnection
class FactoryConnection:

    @classmethod    
    def get_connection(cls, host, data_base, user, password, port, db_type)->Connection:
        if db_type == 'mysql':
            return MysqlConnection.getInstance(host, data_base, user, password, port)
        elif db_type == 'postgresql':
            return PostgresConnection.getInstance(host, data_base, user, password, port)
        else:
            Logger.critical("Database type not supported: {}".format(db_type))
            raise Exception('Database type not supported')
