from typing import Any, Generator

import scrapy

from macro_scrapy.items import MacroScrapyItem

# musi byt predelano tak aby se dynamicky menila stranka ze ktere jsou stahovana data

class SavingsSpider(scrapy.Spider):
    name = "Savings"

    def start_requests(self) -> Generator[Any, Any, Any]:
        urls = [
            "https://www.czso.cz/csu/czso/cri/ctvrtletni-sektorove-ucty-3-ctvrtleti-2023"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: str) -> Generator[Any, Any, Any]:
        file_extension = ".xlsx"
        file_title = "Savings" + file_extension
        file_url = response.xpath("//a[@href='https://www.czso.cz/documents/11350/191095591/csu010524_1.xlsx/a0a3e0bc-794f-4d20-b085-5d95d3505dba?version=1.0']/@href").get()
        file_url = response.urljoin(file_url)
        item = MacroScrapyItem()
        item["file_urls"] = [file_url]
        item["original_file_name"] = [file_title]
        yield item
