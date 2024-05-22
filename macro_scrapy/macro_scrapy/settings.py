"""Module for settings of scrapy spiders."""
from datetime import datetime as dt
from pathlib import Path

CURRENT_DATE = dt.today().strftime('%Y%m%d')
INPUT_FOLDER = Path(
    '/workspaces/macro_scrapy/data/{0}/input'.format(CURRENT_DATE),
    )
OUTPUT_FOLDER = Path(
    '/workspaces/macro_scrapy/data/{0}/output'.format(CURRENT_DATE),
    )
BOT_NAME = 'macro_scrapy'
SPIDER_MODULES = ('macro_scrapy.spiders')
NEWSPIDER_MODULE = 'macro_scrapy.spiders'
ROBOTSTXT_OBEY = False
ITEM_PIPELINES = {  # noqa: WPS407
    'macro_scrapy.pipelines.MacroScrapyPipeline': 1,
}
FILES_STORE = INPUT_FOLDER
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
FEED_EXPORT_ENCODING = 'utf-8'
MEDIA_ALLOW_REDIRECTS = True
