from typing import Any, Generator

import scrapy

from macro_scrapy.items import MacroScrapyItem


class IndustrialEvolutionSpider(scrapy.Spider):
    name = "IndEvo"

    def start_requests(self) -> Generator[Any, Any, Any]:

        urls = [
            "https://www.czso.cz/csu/czso/pru_cr"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: str) -> Generator[Any, Any, Any]:
        file_extension = ".xlsx"
        xid_mapping = {"1725": "M", "1733": "Q", "1801": "Y"}

        for xid, name in xid_mapping.items():
            file_url = response.xpath(f"//a[@class='out' and contains(@href, 'xid={xid}')]/@href").get()

            if file_url:
                file_url = response.urljoin(file_url)
                file_title = f"IndustrialEvolution_{name}" + file_extension

                item = MacroScrapyItem()
                item["file_urls"] = [file_url]
                item["original_file_name"] = [file_title]
                yield item
