# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter
import mimetypes
from datetime import datetime
from pathlib import Path

from scrapy.pipelines.files import FilesPipeline


class MacroScrapyPipeline(FilesPipeline):
    def file_path(self, request, item=None,response=None, info=None):
        date_today = datetime.today().strftime("%Y%m%d")
        media_ext = Path(request.url).suffix
        # Handles empty and wild extensions by trying to guess the
        # mime type then extension or default to empty string otherwise
        #if media_ext not in mimetypes.types_map:
        #    media_ext = ""
        #    media_type = mimetypes.guess_type(request.url)[0]
        #    if media_type:
        #        media_ext = mimetypes.guess_extension(media_type)
        return f"{date_today}_{item["original_file_name"][0]}{media_ext}"
        #file_name: str = datetime.today().strftime("%Y%m%d")+"_"+item["original_file_name"][0]+"_"+request.url.split("/")[-1]
        #return file_name

