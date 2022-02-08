from config import Logger
from scrapy.crawler import CrawlerProcess
from src.domain.doktuz.spiders.doktuz_excel import DoktuzExcel
from src.domain.doktuz import settings as my_settings
from scrapy.settings import Settings


def scrapper_doktuz_excel(init_date:str, end_date:str, by:int):
    '''
     Return data scraped from the Doktuz website between two dates,
     init_date and end_date; further it range is divided by "by" to get the excels one by one.
     Both dates must be in the format dd-mm-yyyy.
     init_date: str
     end_date: str
     by: int
    '''
    try:
        Logger.info("scrapper_doktuz_excel usescase started")
        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)
        process = CrawlerProcess(settings=crawler_settings)
        process.crawl(DoktuzExcel, domain='intranet.doktuz.com', init_date=init_date, end_date=end_date, by=by)
        process.start()
    except Exception as e:
        Logger.error("scrapper_doktuz_excel usescase failed", exc_info=True)
# EJECUCION POR TERMINAL
# scrapy runspider ./src/domain/usecases/get_data.py -o doktuz.csv -t csv 