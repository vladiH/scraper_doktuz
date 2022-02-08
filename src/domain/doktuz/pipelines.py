# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from config import Logger
class DoktuzPipeline:
    def process_item(self, item, spider):
        try:
            if(item['imp']!=None):
                valueImp = re.search(r'\((.*?)\)',item['imp']).group(1).split(',')
                valueImp = "https://intranet.doktuz.com/HistoriasClinicas/PaquetesMedicos/imprimirtodos.php?idcomprobante="+valueImp[0]+"&logo=1&"+"firma="+valueImp[1]+"&consen="+valueImp[2]
                item['imp'] = valueImp
            if(item['certificado']!=None):
                valueImp = item['certificado'].split('/')[2:]
                valueImp.insert(0,'https://intranet.doktuz.com')
                valueImp = '/'.join(valueImp)
                item['certificado'] = valueImp
            return item
        except Exception as e:
            Logger.error('DoktuzPipeline: fail when spider was processing imp value from item: {} '.format(
                item
            ), exc_info=True)
            raise e