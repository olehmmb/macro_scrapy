from typing import Any, Generator

import scrapy

from macro_scrapy.items import MacroScrapyItem


class EurostatSpider(scrapy.Spider):
    name = "Eurostat"

    def start_requests(self) -> Generator[Any, Any, Any]:
        urls = [
            "https://ec.europa.eu/eurostat/data/database"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: str) -> Generator[Any, Any, Any]:
        file_title = file_url = response.xpath("//a[@href='https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/une_rt_m?format=TSV&compressed=true']/@aria-label").get()
        file_url = response.xpath("//a[@href='https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/une_rt_m?format=TSV&compressed=true']/@href").get()
        file_url = response.urljoin(file_url)
        item = MacroScrapyItem()
        item["file_urls"] = [file_url]
        item["original_file_name"] = [file_title]
        yield item
