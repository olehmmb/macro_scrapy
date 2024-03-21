from typing import Any, Generator

import scrapy

from macro_scrapy.items import MacroScrapyItem


class WagesSpider(scrapy.Spider):
    name = "Wages"

    def start_requests(self) -> Generator[Any, Any, Any]:
        urls = [
            "https://www.czso.cz/documents/11350/190537026/gpmz030524.xlsx/387a2ec7-c808-4915-9cdf-0720c82e21d5?version=1.0",
            "https://www.czso.cz/documents/11350/122733562/pmz030821_5.xlsx/1b3900a3-0123-45ee-8c0c-524aca3851bf?version=1.0"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: str) -> Generator[Any, Any, Any]:
        file_extension = ".xlsx"
        xid_mapping = {"190537026": "GrossWage", "122733562": "MedianWage"}
        file_title = ""

        for xid, name in xid_mapping.items():
            if xid in response.url:
                file_title = f"{name}" + file_extension

        file_url_a = response.urljoin(response.url)
        file_url_b = response.urljoin(response.url)

        item = MacroScrapyItem()
        item["file_urls"] = [file_url_a, file_url_b]
        item["original_file_name"] = [file_title]

        yield item
