"""Define the data fields for the items scraped by the spider."""

import scrapy


class MacroScrapyItem(scrapy.Item):
    """Defines the data fields for the items scraped by the spider.

    Attributes:
        file_urls: Field for storing the URLs of the files to be downloaded.
        original_file_name: Field for storing the original names of the files.
        files: Field for storing the paths of the downloaded files.
        table_data: Field for storing the scraped table data.
        month: Field for storing the month associated with the data.
        saldo: Field for storing the saldo information.
    """

    file_urls = scrapy.Field()
    original_file_name = scrapy.Field()
    files = scrapy.Field()
    table_data = scrapy.Field()
    month = scrapy.Field()
    saldo = scrapy.Field()
