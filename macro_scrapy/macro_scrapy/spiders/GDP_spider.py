from typing import Any, Generator

import scrapy

from macro_scrapy.items import MacroScrapyItem


class GDPSpider(scrapy.Spider):
    name = "GDP"

    def start_requests(self) -> Generator[Any, Any, Any]:
        urls = [
            "https://apl.czso.cz/pll/rocenka/rocenkavyber.kvart?mylang=CZ&j=Tab_GS",
            "https://apl.czso.cz/pll/rocenka/rocenkavyber.kvart?mylang=CZ&j=Tab_VS",
            "https://apl.czso.cz/pll/rocenka/rocenkavyber.kvart?mylang=CZ&j=Tab_ZS"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: str) -> Generator[Any, Any, Any]:
        file_extension = ".xlsx"
        xid_mapping = {"GS": "Contributions", "VS": "Expenses", "ZS": "Sources"}
        file_title = ""

        for xid, name in xid_mapping.items():
            if xid in response.url:
                file_title = f"GDP_{name}" + file_extension

        file_url = response.xpath("//a[text()='Stahnout vše v jednom souboru XLSX']/@href").get()  # noqa: E501
        file_url = response.urljoin(file_url)

        item = MacroScrapyItem()
        item["file_urls"] = [file_url]
        item["original_file_name"] = [file_title]
        yield item
