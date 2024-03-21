from typing import Any, Generator

import scrapy

from macro_scrapy.items import MacroScrapyItem


class HouseholdSpider(scrapy.Spider):
    name = "Households"

    def start_requests(self) -> Generator[Any, Any, Any]:
        urls = [
            "https://stats.oecd.org/SDMX-JSON/data/NAAG/.DBTS14_S15NDI/OECD?contentType=csv",
            "https://stats.oecd.org/SDMX-JSON/data/DP_LIVE/CZE.HHDI.GROSS.PC_CHGPPCAP.Q/OECD?contentType=csv"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: str) -> Generator[Any, Any, Any]:
        file_extension = ".csv"
        xid_mapping = {"DBT": "Debt", "HHDI": "DisposableIncome"}
        file_title = ""

        for xid, name in xid_mapping.items():
            if xid in response.url:
                file_title = f"Households_{name}" + file_extension

        file_url_a = response.urljoin(response.url)
        file_url_b = response.urljoin(response.url)

        item = MacroScrapyItem()
        item["file_urls"] = [file_url_a, file_url_b]
        item["original_file_name"] = [file_title]
        yield item
