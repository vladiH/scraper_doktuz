import os
import json
from base64 import b64decode
from config import Config, Logger
from selenium import webdriver
from textwrap import dedent
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class DoktuzSeleniumPipeline:
    def __init__(self,driver_path, local_dir):
        self.driver_path = driver_path
        self.local_dir = local_dir
        self.cookie = None

    def open_spider(self, spider):
        try:
            self.local_dir = self.local_dir + '/pdfs'
            self.create_directory(self.local_dir)
            self.setup_driver()

        except Exception as e:
            Logger.critical("DoktuzSeleniumPipeline.open_spider: fail when spider was opening selenium driver", exc_info=True)
            raise e
    def setup_driver(self):
        try:
            chrome_options = webdriver.ChromeOptions()
            settings = {"recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
            "selectedDestinationId": "Save as PDF", "version": 2}
            prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings),
            'savefile.default_directory': self.local_dir}
            chrome_options.add_experimental_option('prefs', prefs)
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--single-process')
            if Config.HIDDEN:
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--kiosk-printing')
            
            self.driver = webdriver.Chrome(executable_path=self.driver_path, options=chrome_options)
            self.driver.set_page_load_timeout(120)
            self.driver.set_script_timeout(120)
        except Exception as e:
            raise e

    def close_spider(self, spider):
        self.driver.quit()
        
    @classmethod
    def from_crawler(cls, crawler):
        dp = Config.DRIVER_PATH
        return cls(
            driver_path=dp,
            local_dir = os.getcwd()
        )

    async def process_item(self, item, spider):
        try:
            if item!= None:
                Logger.info("Processing item: {}".format(item))
                if(self.cookie==None or self.driver.get_cookies()==[]):
                    self.cookie = item['cookie'].split('=')
                    self.driver.get('https://intranet.doktuz.com/Resultados/Empresa/resultados.php')
                    self.driver.delete_all_cookies()
                    self.driver.add_cookie({'name': self.cookie[0], 'value': self.cookie[1], 
                    'domain': 'intranet.doktuz.com', 'path': '/'})
                if(not self.driver.get_cookies()):
                    Logger.warning('DoktuzSeleniumPipeline.process_item: pdf has not been processed, not cookies. {}'.format(item))
                else:
                    dir_name = self.local_dir+'/'+item['codigo']
                    if('imp' in item and item['imp_downloaded']==False):
                        self.page_as_pdf(item['imp'],dir_name,item['codigo']+"-imp.pdf")
                        item['imp_downloaded'] = True
                        item['imp'] = item['codigo']+"-imp.pdf"
                    if('certificado' in item and item['certificado_downloaded']==False):
                        self.page_as_pdf(item['certificado'],dir_name,item['codigo']+"-certificado.pdf")
                        item['certificado_downloaded'] = True
                        item['certificado'] = item['codigo']+"-certificado.pdf"
                #del item['cookie']
                #return item
        except Exception as e:
            Logger.error('DoktuzSeleniumPipeline.process_item: pdf has not been processed. {}, error:{}'.format(item, e))
            self.setup_driver()
            Logger.warning('DoktuzSeleniumPipeline.page_as_pdf: driver seccessfully restarted')
        finally:
            item.pop('cookie', None)
            return item

    def page_as_pdf(self, link, dir_name, file_name):
        try:
            self.driver.get(link)
            #self.wait_for_ajax()
            self.wait_for_loading_fade()
            self.wait_until_images_loaded(self.driver)
            #self.create_directory(dir_name)
            if Config.HIDDEN:
                self.print_headless_page(file_name, link)
            else:
                self.print_page(file_name)
        except Exception as e:
            Logger.error('conversion error: {}'.format(e))  
           

    def wait_for_ajax(self):
        wait = WebDriverWait(self.driver, 15)
        try:
            wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        except Exception as e:
            Logger.error('waiting error, ajax code error {}'.format(e))
            raise e

    def wait_for_loading_fade(self):
        try:
            #elements = self.driver.find_elements(by=By.CLASS_NAME, value='FacetDataTDM14')
            WebDriverWait(self.driver, 120).until_not(EC.text_to_be_present_in_element((By.CLASS_NAME,'FacetDataTDM14'), "Cargando..."))
        except Exception as e:
            Logger.error('waiting error, loading fade error {}'.format(e))
            #raise e
        
    def print_page(self, file_name):
        try:
            self.driver.execute_script('document.title="{}";'.format(file_name)); 
            self.driver.execute_script("window.print();")
        except Exception as e:
            Logger.error('printing PDF error {}'.format(e))
            #raise e
    def print_headless_page(self, file_name, link):
        try:
            page = self.driver.execute_cdp_cmd( "Page.printToPDF", {"path": link, "format": 'A4'})
            # Define the Base64 string of the PDF file
            b64 = page['data']

            # Decode the Base64 string, making sure that it contains only valid characters
            bytes = b64decode(b64, validate=True)

            # Perform a basic validation to make sure that the result is a valid PDF file
            # Be aware! The magic number (file signature) is not 100% reliable solution to validate PDF files
            # Moreover, if you get Base64 from an untrusted source, you must sanitize the PDF contents
            if bytes[0:4] != b'%PDF':
                raise ValueError('Missing the PDF file signature')
            # Write the PDF contents to a local file
            f = open(self.local_dir+'/'+file_name, 'wb')
            f.write(bytes)
            f.close()
        except Exception as e:
            Logger.error('printing headless PDF error {}'.format(e))
            #raise e
    
    def create_directory(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            Logger.error('creation error, creating directory', exc_info=True)
            raise e

    def wait_until_images_loaded(self, driver, timeout=120):
        try:
            elements = self.driver.find_elements(by=By.TAG_NAME, value='img')
            WebDriverWait(self.driver, timeout).until(lambda wd:self.all_array_elements_are_true(wd,elements) )
        except Exception as e:
            Logger.error('waiting image error  {}'.format(e))
            raise e

    def all_array_elements_are_true(self,driver, elements):
        array = [driver.execute_script("return arguments[0].complete", img) for img in elements]
        for element in array:
            if not element:
                return False
        return True