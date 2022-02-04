import os
import logging.config
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.domain.doktuz.spiders.doktuz import Doktuz
from src.domain.doktuz import settings as my_settings
from scrapy.settings import Settings
from pyvirtualdisplay import Display
if __name__ == "__main__": # EJECUCION POR INTERFAZ GRAFICA
    # Configure the logger
    # loggerConfigFileName: The name and path of your configuration file
    logging.config.fileConfig(os.path.normpath('config.ini'))

    # Create the logger
    # Admin_Client: The name of a logger defined in the config file
    mylogger = logging.getLogger('dev')
    display = Display(visible=0, size=(800, 600))
    display.start()
    crawler_settings = Settings()
    crawler_settings.setmodule(my_settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(Doktuz, domain='intranet.doktuz.com')
    process.start()      
    display.stop()
    logging.shutdown()
# EJECUCION POR TERMINAL
# scrapy runspider ./src/domain/usecases/get_data.py -o doktuz.csv -t csv 