import csv
from typing import Any, Generator

import scrapy
from scrapy.utils.project import get_project_settings


class TableSpider(scrapy.Spider):
    name = 'tables_spider'

    def start_requests(self) -> Generator[Any, Any, Any]:
        url = 'url'
        xpath = 'xpath'
        urls = {
            'CNB_EUR_CZK': {
                url: 'https://www.cnb.cz/en/financial-markets/foreign-exchange-market/central-bank-exchange-rate-fixing/central-bank-exchange-rate-fixing/currency_average.html?currency=EUR',
                xpath: [],
                'xpath_table': ['(//table)[1]/tr'],
                },
            'czso_inflace': {
                url: 'https://www.czso.cz/csu/czso/mira_inflace',
                xpath: [],
                'xpath_table': ['(//table)[2]//tbody/tr[position() > last() - 6]'],
                },
        }

        for name, value in urls.items():
            yield scrapy.Request(url=value[url], callback=self.parse_xpath, dont_filter=True, cb_kwargs={'name': name, 'xpath': value[xpath], 'xpath_table': value['xpath_table'][0]})

    def parse_xpath(self, response: scrapy.http.response.Response, name: str, xpath: list[str], xpath_table: str) -> Generator[Any, Any, Any]:
        curr_xpath = xpath.pop(0) if xpath else None
        new_links = response.xpath(curr_xpath).getall() if curr_xpath else [response.url]
        for new_link in new_links:
            yield scrapy.Request(url=response.urljoin(new_link), dont_filter=True, callback=self.parse_table if not xpath else self.parse_xpath, cb_kwargs={'name': name, 'xpath': xpath, 'xpath_table': xpath_table})

    def parse_table(self, response: scrapy.http.response.Response, name: str, xpath: None, xpath_table: str) -> None:
        table_xpath = xpath_table
        file_path = '{0}/{1}_{2}.csv'.format(
            get_project_settings().get('FILES_STORE'),
            get_project_settings().get('CURRENT_DATE'),
            name,
        )
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in response.xpath(table_xpath):
                table_row = row.xpath('td//text() | th//text()').getall()
                writer.writerow(table_row)
