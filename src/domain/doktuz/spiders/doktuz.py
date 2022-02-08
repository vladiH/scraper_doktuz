import scrapy
from config import Config, Logger
from scrapy.http import Response, Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from src.domain.doktuz.items import DoktuzItem
class Doktuz(CrawlSpider):
  #name = 'Doktuz'
  # custom_settings = {
  #   'USER_AGENT': ,
  #   #'CLOSESPIDER_PAGECOUNT': 3
  # }
  
  allowed_domains = ["intranet.doktuz.com"]

  #download_delay = 1

  rules = ( 
    Rule(
      LinkExtractor( 
        allow=r'page=', 
        allow_domains=('intranet.doktuz.com'),
      ), follow=True, callback='parse_data',),
  )

  def __init__(self, *args, **kwargs):
    self.init_date = kwargs['init_date']
    self.end_date = kwargs['end_date']
    self.name = kwargs['name']
    self.start_urls = []
    super(Doktuz, self).__init__(*args, **kwargs) 

  @classmethod
  def from_crawler(cls, crawler, *args, **kwargs):
    spider = cls(
      init_date = kwargs['init_date'],
      end_date = kwargs['end_date'],
      name = crawler.settings.get('BOT_NAME'),
    )
    spider._follow_links = crawler.settings.getbool('CRAWLSPIDER_FOLLOW_LINKS', True)
    spider.crawler = crawler
    return spider

  def start_requests(self):
    try:
      return [scrapy.FormRequest("https://intranet.doktuz.com/index.php?usuario={}&pass={}&btnenviar=Aceptar".format(Config.DOKTUZ_USERNAME,Config.DOKTUZ_PASSWORD),
                               formdata={},
                               callback=self.parse_resultados)]
    except Exception as e:
      Logger.critical('Doktuz.start_requests: fail when spider was starting', exc_info=True)
                               
  def parse_resultados(self, response:Response):
    Logger.info('Doktuz.parse_resultados: init_date {}, end_date {} '.format(self.init_date, self.end_date))
    self.cookie = response.request.headers.getlist('Cookie')[0].decode('utf-8')
    return Request(response.url+'?fechafinal={}&fechainicio={}&dnip=&descripcion=&proyecto=&idempresa4='.format(self.end_date, self.init_date))                            
  
  def parse_data(self, response:Response):
    try:
      sel = Selector(response)
      rows = sel.xpath('//div[@id="tabs-1"]/table/tr[3]/td/table/tr[@class="FacetFilaTD"]')
      for row in rows:
        item = ItemLoader(DoktuzItem(), row)
        #cod = row.xpath("td[2]/div/text()").get()
        item.add_xpath('codigo', "td[2]/div/text()")
        item.add_xpath('fecha', "td[3]/text()")
        item.add_xpath('empresa', "td[4]/text()")
        item.add_xpath('subcontrata', "td[5]/text()")
        item.add_xpath('proyecto', "td[6]/text()")
        item.add_xpath('t_exam', "td[7]/text()")
        item.add_xpath('paciente', "td[8]/div/text()")
        valueImp = row.xpath('td[35]/a/@onclick').get()
        valueCertificado = row.xpath('td[27]/div/a/@href').get()
        item.add_value('certificado',valueCertificado)
        item.add_value('certificado_downloaded', False)
        item.add_value('imp', valueImp)
        item.add_value('imp_downloaded', False)
        item.add_value('cookie', self.cookie)
        yield item.load_item()
    except Exception as e:
      Logger.error('Doktuz.parse_data: fail when spider was recovering data from '+ response.url, exc_info=True)
      raise e
  '''def parse_pdf_page(self, response:Response):
    sel = Selector(response)
    self.logger.info("parse_pdf_page")
    with open("out.html", 'wb') as html_file:
      html_file.write(response.body)

  def errback_httpbin(self, failure):
    self.logger.info("errback_httpbin", failure)
    print(failure)

  def check_folder(dir_name):
    return os.path.isdir(dir_name)'''

  

