import logging.config
from config import Logger
from src.domain.usecases.scraper_doktuz import scrapper_doktuz
from src.domain.usecases.scraper_doktuz_excel import scrapper_doktuz_excel
if __name__ == "__main__": # EJECUCION POR INTERFAZ GRAFICA
    Logger.warning("App started")
    #scrapper_doktuz('01-01-2022', '27-01-2022')
    scrapper_doktuz_excel('25-01-2022', '08-02-2022', 7)
    logging.shutdown()
# EJECUCION POR TERMINAL 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
# scrapy runspider ./src/domain/usecases/get_data.py -o doktuz.csv -t csv 