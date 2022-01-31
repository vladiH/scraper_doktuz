
import sqlalchemy
from infrastruture.external.factory_db import FactoryDataBase
from sqlalchemy import create_engine

class PostgresConnection(FactoryDataBase):
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
        

    def connect(self):
        try:
            url = 'postgresql://{user}:{passwd}@{host}:{port}/{db}'.format(
            user=self.user, passwd=self.password, host=self.host, port=self.port, db=self.data_base)
            self.engine = create_engine(url, pool_size = 5)
            return True
        except sqlalchemy.exc.OperationalError:
                return False

    def execute(self, query):
        try:
            self.engine.execute(query)
        except sqlalchemy.exc.ProgrammingError as e:
            raise sqlalchemy.exc.SQLAlchemyError(e)
