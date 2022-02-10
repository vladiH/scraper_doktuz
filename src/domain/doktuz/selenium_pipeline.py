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
            chrome_options = webdriver.ChromeOptions()
            settings = {"recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
            "selectedDestinationId": "Save as PDF", "version": 2}
            prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings),
            'savefile.default_directory': self.local_dir}
            chrome_options.add_experimental_option('prefs', prefs)
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            if Config.HIDDEN:
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--kiosk-printing')
            
            self.driver = webdriver.Chrome(executable_path=self.driver_path, options=chrome_options)
        except Exception as e:
            Logger.critical("DoktuzSeleniumPipeline.open_spider: fail when spider was opening selenium driver", exc_info=True)
            raise e

    def close_spider(self, spider):
        self.driver.close()
        
    @classmethod
    def from_crawler(cls, crawler):
        dp = Config.DRIVER_PATH
        return cls(
            driver_path=dp,
            local_dir = os.getcwd()
        )

    async def process_item(self, item, spider):
        try:
            Logger.info("Processing item: {}".format(item))
            if(self.cookie==None):
                self.cookie = item['cookie'].split('=')
                self.driver.get(item['imp'])
                self.driver.delete_all_cookies()
                self.driver.add_cookie({'name': self.cookie[0], 'value': self.cookie[1], 
                'domain': 'intranet.doktuz.com', 'path': '/', 'Expires': 'Session'})
            if(not self.driver.get_cookies()):
                Logger.warning('DoktuzSeleniumPipeline.process_item: pdf has not been processed, not cookies. {}'.format(item))
            else:
                dir_name = self.local_dir+'/'+item['codigo']
                if(item['imp']!=None):
                    self.page_as_pdf(item['imp'],dir_name,item['codigo']+"-imp.pdf")
                    item['imp_downloaded'] = True
                    item['imp'] = item['codigo']+"-imp.pdf"
                if(item['certificado']!=None):
                    self.page_as_pdf(item['certificado'],dir_name,item['codigo']+"-certificado.pdf")
                    item['certificado_downloaded'] = True
                    item['certificado'] = item['codigo']+"-certificado.pdf"
        except Exception as e:
            Logger.error('DoktuzSeleniumPipeline.process_item: pdf has not been processed. {}'.format(item), exc_info=True)
        finally:
            del item['cookie']
            return item
    def page_as_pdf(self, link, dir_name, file_name):
        try:
            self.driver.get(link)
            #self.wait_for_ajax()
            self.wait_for_loading_fade()
            self.wait_until_images_loaded(self.driver)
            #self.create_directory(dir_name)
            if Config.HIDDEN:
                self.print_page(file_name)
            else:
                self.print_headless_page(file_name, link)
        except Exception as e:
            Logger.error('conversion error')
            raise e   

    def wait_for_ajax(self):
        wait = WebDriverWait(self.driver, 15)
        try:
            wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        except Exception as e:
            Logger.error('waiting error, ajax code error')
            raise e

    def wait_for_loading_fade(self):
        try:
            #elements = self.driver.find_elements(by=By.CLASS_NAME, value='FacetDataTDM14')
            WebDriverWait(self.driver, 30).until_not(EC.text_to_be_present_in_element((By.CLASS_NAME,'FacetDataTDM14'), "Cargando..."))
        except Exception as e:
            Logger.error('waiting error, loading fade error')
            raise e
        
    def print_page(self, file_name):
        try:
            self.driver.execute_script('document.title="{}";'.format(file_name)); 
            self.driver.execute_script("window.print();")
        except Exception as e:
            Logger.error('printing PDF error')
            raise e
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
            Logger.error('printing headless PDF error')
            raise e
    
    def create_directory(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            Logger.error('creation error, creating directory', exc_info=True)
            raise e

    def wait_until_images_loaded(self, driver, timeout=30):
        try:
            elements = self.driver.find_elements(by=By.TAG_NAME, value='img')
            WebDriverWait(self.driver, 30).until(lambda wd:self.all_array_elements_are_true(wd,elements) )
        except Exception as e:
            Logger.error('waiting image error ')
            raise e

    def all_array_elements_are_true(self,driver, elements):
        array = [driver.execute_script("return arguments[0].complete", img) for img in elements]
        for element in array:
            if not element:
                return False
        return True