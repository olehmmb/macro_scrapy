from datetime import datetime as dt
from datetime import timedelta, timezone
from typing import Any, Generator

import scrapy

from macro_scrapy.items import MacroScrapyItem

current_date = dt.now(tz=timezone.utc)
last_month = current_date - timedelta(days=current_date.day)
last_month_adj = last_month.strftime("%Y/%m")

class UnemploymentMPSVSpider(scrapy.Spider):
    name = "Unemployment"

    def start_requests(self) -> Generator[Any, Any, Any]:
        urls = [
            "https://www.mpsv.cz/web/cz/mesicni"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: str) -> Generator[Any, Any, Any]:
        file_extension = ".zip"
        file_title = "Unemployment_MPSV" + file_extension
        file_url = response.xpath(f"//a[@class='download-icon' and contains(@href, '{last_month_adj}')]/@href").get()
        file_url = response.urljoin(file_url)
        item = MacroScrapyItem()
        item["file_urls"] = [file_url]
        item["original_file_name"] = [file_title]
        yield item
