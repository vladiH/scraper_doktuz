import scrapy
import datetime
from config import Config, Logger
from scrapy.http import Response, Request
from scrapy.spiders import Spider
class DoktuzExcel(Spider):
  
  allowed_domains = ["intranet.doktuz.com"]

  def __init__(self, *args, **kwargs):
    self.init_date = kwargs['init_date']
    self.end_date = kwargs['end_date']
    self.by = kwargs['by']
    self.name = kwargs['name']
    self.start_urls = []
    super(DoktuzExcel, self).__init__(*args, **kwargs) 

  @classmethod
  def from_crawler(cls, crawler, *args, **kwargs):
    spider = cls(
      init_date = kwargs['init_date'],
      end_date = kwargs['end_date'],
      by = kwargs['by'],
      name = crawler.settings.get('BOT_NAME'),
    )
    spider._follow_links = crawler.settings.getbool('CRAWLSPIDER_FOLLOW_LINKS', True)
    spider.crawler = crawler
    return spider

  def start_requests(self):
    try:
      return [scrapy.FormRequest("https://intranet.doktuz.com/index.php?usuario={}&pass={}&btnenviar=Aceptar".format(Config.DOKTUZ_USERNAME,Config.DOKTUZ_PASSWORD),
                               formdata={},
                               callback=self.parse)]
    except Exception as e:
      Logger.critical('DoktuzExcel.start_requests: fail when spider was starting', exc_info=True)
                               
  def parse(self, response:Response):
    Logger.info('DoktuzExcel.parse_resultados: init_date {}, end_date {} '.format(self.init_date, self.end_date))
    self.cookie = response.request.headers.getlist('Cookie')[0].decode('utf-8')
    url_base = 'https://intranet.doktuz.com/Resultados/Empresa/excel_reporte_vigilancia.php?'
    date_1 = datetime.datetime.strptime(self.init_date.replace('-','/'), "%d/%m/%Y")
    date_2 = datetime.datetime.strptime(self.end_date.replace('-','/'), "%d/%m/%Y")
    while date_1 <= date_2:
      end_date = date_1 + datetime.timedelta(days=self.by)
      yield {'url':url_base+'?fechafinal={}&fechainicio={}&dnip=&descripcion=&proyecto=&idempresa4='.format( end_date.strftime('%d-%m-%Y'), date_1.strftime('%d-%m-%Y'),)}
      date_1 = end_date

                  
  

  

