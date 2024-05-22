"""Module with Scrapy spider for scraping data from the MFCR website."""
import csv

from macro_scrapy.items import MacroScrapyItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.project import get_project_settings


class ScrapemeSpider(CrawlSpider):
    """A Scrapy spider for scraping data from the MFCR website.

    Attributes:
        name (str): The name of the spider.
        allowed_domains (list): A list of domains allowed to crawl.
        start_urls (list): A list of URLs where the spider begins to crawl.
        rules (tuple): A collection of one or more Rule objects.
    """

    name = 'gov_debt'
    allowed_domains = ['www.mfcr.cz']
    start_urls = ['https://www.mfcr.cz/cs/rozpoctova-politika/statni-rozpocet/plneni-statniho-rozpoctu']
    file_path = '{0}/{1}_MFCR_state_deficit.csv'.format(
        get_project_settings().get('FILES_STORE'),
        get_project_settings().get('CURRENT_DATE'),
        )
    custom_settings = {
        'FEEDS': {file_path: {
            'format': 'csv',
            'item_export_kwargs': {
                'include_headers_line': False,
                'quoting': csv.QUOTE_NONE,
                'escapechar': ' ',
                'delimiter': ';',
                },
            },
                },
        'FEED_EXPORT_FIELDS': ['table_data'],
    }

    rules = (Rule(
        LinkExtractor(
            allow=r'plneni-statniho-rozpoctu\/(20(1[8-9]|[2-9][0-9]))\/mesicni-pokladni-plneni(-sr-)?[^\/]+$',
            ),
        callback='parse_table',
        follow=True,
        ),
    )

    def parse_table(self, response):
        """Process the responses and yield an item for each row in table.

        Args:
            response (obj): The response object to be processed.

        Yields:
            MacroScrapyItem: An item that contains data from a row
              in the table.
        """
        year = response.url.split('plneni-statniho-rozpoctu/')[1].split(
            '/mesicni-pokladni-plneni',
            )[0]
        table_xpath = '//table[contains(.,"ní státního rozpočtu v roce")]/*/tr'
        for row in response.xpath(table_xpath):
            table_item = MacroScrapyItem()
            table_row = row.xpath(
                'td//text()[not(.="\xa0")] | th//text()[not(.="\xa0")]',
                ).getall()
            if len(table_row) > 1:
                table_row.append(year)
                table_row = [field.replace(',', '.') for field in table_row]
                table_row = ','.join(table_row)
                table_item['table_data'] = table_row
                yield table_item
