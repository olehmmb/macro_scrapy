from typing import Any, Generator

import scrapy

from macro_scrapy.items import MacroScrapyItem


class ForeignTradeSpider(scrapy.Spider):
    name = "Foreign"

    def start_requests(self) -> Generator[Any, Any, Any]:
        urls = [
        "https://vdb.czso.cz/vdbvo2/faces/cs/xlsexp?page=vystup-objekt&z=T&f=TABULKA&skupId=2848&katalog=32935&pvo=VZO011-NP-D&str=str(236)",
        "https://vdb.czso.cz/vdbvo2/faces/cs/xlsexp?page=vystup-objekt&z=T&f=TABULKA&skupId=2848&katalog=32935&pvo=VZO011-NP-C&str=str(395)",
        "https://vdb.czso.cz/vdbvo2/faces/cs/xlsexp?page=vystup-objekt&z=T&f=TABULKA&skupId=2848&katalog=32935&pvo=VZO011-NP-B&str=str(153)"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: str) -> Generator[Any, Any, Any]:
        file_extension = ".xlsx"
        xid_mapping = {"236": "M", "395": "Q", "153": "Y"}

        for xid, name in xid_mapping.items():
            if f"str({xid})" in response.url:
                file_title = f"ForeignTrade_{name}" + file_extension

        file_url_m = response.urljoin(response.url)
        file_url_q = response.urljoin(response.url)
        file_url_y = response.urljoin(response.url)

        item = MacroScrapyItem()
        item["file_urls"] = [file_url_m, file_url_q, file_url_y]
        item["original_file_name"] = [file_title]

        yield item
