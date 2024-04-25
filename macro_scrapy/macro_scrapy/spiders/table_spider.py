from typing import Any, Generator

import scrapy
from scrapy.utils.project import get_project_settings

from macro_scrapy.items import MacroScrapyItem
from macro_scrapy.settings import CURRENT_DATE


class TableSpider(scrapy.Spider):
    name = "table_spider"
    custom_settings = {
        "FEEDS": {get_project_settings().get("FILES_STORE") /  fr"{CURRENT_DATE}_MFCR_state_deficit.csv": {"format": "csv",
                                  "overwrite": True,
                                  "store_empty": True}}
        }
    def start_requests(self) -> Generator[Any, Any, Any]:
        urls = {
            "MFCR_state_deficit.csv":{"url":"https://www.mfcr.cz/cs/rozpoctova-politika/statni-rozpocet/plneni-statniho-rozpoctu",
                                   "xpath":"//h3[@class='b-article__title h4']//a[contains(@class, 'b-') and contains(@href, '/mesicni-pokladni-plneni')]/@href"}

        }
        for name, value in urls.items():
            yield scrapy.Request(url=value["url"],callback=self.parse,dont_filter=True,cb_kwargs = {"name":name, "xpath":value["xpath"]})

    def parse(self, response: scrapy.http.response.Response, name: str, xpath: str) -> Generator[Any, Any, Any]:
        new_link = response.xpath(xpath).get()
        yield scrapy.Request(url = response.urljoin(new_link), callback = self.parse_table)

    def parse_table(self, response) -> Generator:
        for row in response.xpath("//table[caption[contains(text(),'Měsíční pokladní plnění státního rozpočtu v roce')]]//tbody/tr"):
            yield {
                "Month" : row.xpath("th//text()").get(),
                "Saldo": row.xpath("td[3]//text()").get(),
            }
