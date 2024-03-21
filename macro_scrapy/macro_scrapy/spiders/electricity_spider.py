import re
from datetime import datetime as dt
from datetime import timedelta, timezone
from typing import Any, Generator

import scrapy

from macro_scrapy.items import MacroScrapyItem

current_date = dt.now(tz=timezone.utc)
last_month = current_date - timedelta(days=current_date.day)
last_month_adj = last_month.strftime("%Y/%m")

class ElectricitySpider(scrapy.Spider):
    name = "Electricity"

    def start_requests(self) -> Generator[Any, Any, Any]:
        urls = [
            "https://www.ote-cr.cz/cs/statistika/rocni-zprava?date=%7Bstr(currentYear-1)%7D-01-01"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: str) -> Generator[Any, Any, Any]:
        file_extension = ".zip"
        file_title = "Electricity" + file_extension
        file_url = re.sub(r"^/pubweb/", "", response.xpath("//a[contains(text(),'Rocni_zprava_o_trhu_2024_V0.zip')]/@href").get())
        file_url = response.urljoin(file_url)

        item = MacroScrapyItem()
        item["file_urls"] = [file_url]
        item["original_file_name"] = [file_title]
        yield item
