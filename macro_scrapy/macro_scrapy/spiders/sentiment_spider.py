from typing import Any, Generator

import scrapy

from macro_scrapy.items import MacroScrapyItem


class SentimentSpider(scrapy.Spider):
    name = "Sentiment"

    def start_requests(self) -> Generator[Any, Any, Any]:
        urls = [
            "https://www.czso.cz/csu/czso/cri/konjunkturalni-pruzkumy-leden-2024"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: str) -> Generator[Any, Any, Any]:
        file_extension = ".xlsx"
        file_title = "Sentiment" + file_extension
        file_url = response.xpath("//a[@href='https://www.czso.cz/documents/11350/218351664/gkpr012424_5.xlsx/c4b9fb47-f5db-4b6a-9e1a-88f1c8efbdff?version=1.0']/@href").get()
        file_url = response.urljoin(file_url)

        item = MacroScrapyItem()
        item["file_urls"] = [file_url]
        item["original_file_name"] = [file_title]
        yield item
