from config import Logger
from scrapy.crawler import CrawlerProcess
from src.domain.doktuz.spiders.doktuz import Doktuz
from src.domain.doktuz import settings as my_settings
from scrapy.settings import Settings


def scrapper_doktuz(init_date:str, end_date:str):
    '''
     Return scraped data from Doktuz website between two dates, init_date and end_date.
     Both dates must be in the format dd-mm-yyyy.
     init_date: str
     end_date: str
    '''
    try:
        Logger.info("scrapper_doktuz usescase started")
        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)
        process = CrawlerProcess(settings=crawler_settings)
        process.crawl(Doktuz, domain='intranet.doktuz.com', init_date=init_date, end_date=end_date)
        process.start()
    except Exception as e:
        Logger.error("scrapper_doktuz usescase failed", exc_info=True)
# EJECUCION POR TERMINAL
# scrapy runspider ./src/domain/usecases/get_data.py -o doktuz.csv -t csv 