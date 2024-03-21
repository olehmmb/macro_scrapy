from typing import Any, Generator

import scrapy

from macro_scrapy.items import MacroScrapyItem


class RetailSpider(scrapy.Spider):
    name = "Retail"

    def start_requests(self) -> Generator[Any, Any, Any]:

        urls = [
            "https://vdb.czso.cz/pll/eweb/vdb2xls.export?xid=730",
            "https://vdb.czso.cz/pll/eweb/vdb2xls.export?xid=761",
            "https://vdb.czso.cz/pll/eweb/vdb2xls.export?xid=769"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: str) -> Generator[Any, Any, Any]:
        file_extension = ".xlsx"
        xid_mapping = {"730": "M", "761": "Q", "769": "Y"}
        file_title = ""

        for xid, name in xid_mapping.items():
            if xid in response.url:
                file_title = f"Retail_{name}" + file_extension

        file_url_m = response.urljoin(response.url)
        file_url_q = response.urljoin(response.url)
        file_url_y = response.urljoin(response.url)

        item = MacroScrapyItem()
        item["file_urls"] = [file_url_m, file_url_q, file_url_y]
        item["original_file_name"] = [file_title]

        yield item
