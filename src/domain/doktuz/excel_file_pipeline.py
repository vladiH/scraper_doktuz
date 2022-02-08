import os
import scrapy
from urllib.parse import urlparse
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline

class ExcelFilePipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        original_path = super(ExcelFilePipeline, self).file_path(request, response=None, info=None)
        sha1_and_extension = original_path.split('/')[1] # delete 'full/' from the path
        return request.meta.get('filename','') + "_" + sha1_and_extension+'.xlsx'
    
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['url'])
    
    def item_completed(self, results, item, info):
        file_paths = [self.store.basedir+'/'+ x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
        adapter = ItemAdapter(item)
        adapter['file_paths'] = file_paths
        return item