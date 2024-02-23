# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from datetime import datetime

class MacroScrapyPipeline(FilesPipeline):
    def file_path(self, request, item=None,response=None, info=None):
        file_name: str = datetime.today().strftime("%Y%m%d")+"_"+item["original_file_name"][0]+"_"+request.url.split("/")[-1]
        return file_name
