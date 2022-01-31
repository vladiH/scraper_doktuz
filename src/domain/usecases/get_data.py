import scrapy
import re
import os
import pdfkit
from scrapy.http import Response, Request
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess

from selenium.webdriver import Chrome

class DoktuzData(Item):
  codigo = Field()
  fecha = Field()
  empresa = Field()
  subcontrata = Field()
  proyecto = Field()
  t_exam = Field()
  paciente = Field()
  #imp = Field()

class Doktuz(CrawlSpider):
  name = 'Doktuz'
  custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
    #'CLOSESPIDER_PAGECOUNT': 3
  }

  allowed_domains = ["intranet.doktuz.com"]
  start_urls = []

  download_delay = 1

  rules = ( 
    Rule(
      LinkExtractor( 
        allow=r'page=', 
        allow_domains=('intranet.doktuz.com'),
      ), follow=True, callback='parse_data',),
  )

  def start_requests(self):
    return [scrapy.FormRequest("https://intranet.doktuz.com/index.php?usuario=PPAMOLSA&pass=PPAMOLSA&btnenviar=Aceptar",
                               formdata={'usuario': 'PPAMOLSA', 'pass': 'PPAMOLSA'},
                               callback=self.parse_resultados)]
                               
  def parse_resultados(self, response:Response):
    self.logger.info(response.url)
    #print(response.)
    return Request(response.url+'?fechafinal=27-01-2022&fechainicio=01-01-2022&dnip=&descripcion=&proyecto=&idempresa4=')                            
  
  def parse_data(self, response:Response):
    sel = Selector(response)
    rows = sel.xpath('//div[@id="tabs-1"]/table/tr[3]/td/table/tr[@class="FacetFilaTD"]')
    for row in rows:
      item = ItemLoader(DoktuzData(), row)
      item.add_xpath('codigo', "td[2]/div/text()")
      item.add_xpath('fecha', "td[3]/text()")
      item.add_xpath('empresa', "td[4]/text()")
      item.add_xpath('subcontrata', "td[5]/text()")
      item.add_xpath('proyecto', "td[6]/text()")
      item.add_xpath('t_exam', "td[7]/text()")
      item.add_xpath('paciente', "td[8]/div/text()")
      valueImp = row.xpath('td[35]/a/@onclick').get()
      #yield item.load_item()
      if(valueImp!=None):
        valueImp = re.search(r'\((.*?)\)',valueImp).group(1).split(',')[0]
        valueImp = "https://intranet.doktuz.com/HistoriasClinicas/PaquetesMedicos/imprimirtodos.php?idcomprobante="+valueImp
        yield Request(url=valueImp, callback=self.parse_pdf_page,errback=self.errback_httpbin, cb_kwargs={'item': item.load_item()}) 

  #TODO:NUNCA LLEGA A ESTE MODULO
  def parse_pdf_page(self, response:Response, item):
    sel = Selector(response)
    self.logger.info("parse_pdf_page")
    with open("out.html", 'wb') as html_file:
      html_file.write(response.body)
    yield item

  def errback_httpbin(self, failure):
    self.logger.info("errback_httpbin", failure)
    print(failure)

  def check_folder(dir_name):
    return os.path.isdir(dir_name)

if __name__ == "__main__": # EJECUCION POR INTERFAZ GRAFICA
    process = CrawlerProcess({
      'FEED_FORMAT': 'json',
      'FEED_URI': 'output.json'
    })
    process.crawl(Doktuz)
    process.start()      
# EJECUCION POR TERMINAL
# scrapy runspider ./src/domain/usecases/get_data.py -o doktuz.csv -t csv 