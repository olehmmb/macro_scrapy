from typing import Any, Generator

import scrapy

from macro_scrapy.items import MacroScrapyItem


class NotUsedWagesSpider(scrapy.Spider):
    name = "NotUsedWages"

    def start_requests(self) -> Generator[Any, Any, Any]:
        urls = [
            "https://apl.czso.cz/pll/rocenka/rocenkavyber.kvart?mylang=CZ&j=Tab_M",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: str) -> Generator[Any, Any, Any]:
        file_extension = ".xlsx"
        file_title = "Wages" + file_extension
        file_url = response.xpath("//a[text()='Stahnout vše v jednom souboru XLSX']/@href").get()
        file_url = response.urljoin(file_url)
        item = MacroScrapyItem()
        item["file_urls"] = [file_url]
        item["original_file_name"] = [file_title]
        yield item
