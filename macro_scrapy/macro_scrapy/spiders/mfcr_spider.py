from __future__ import annotations

from typing import Any, Generator

import scrapy

from macro_scrapy.items import MacroScrapyItem


class GDPSpider(scrapy.Spider):
    name = "mfcr_spider"

    def start_requests(self) -> Generator[Any, Any, Any]:
        urls = {
            "MFCR_Makroekonomicka_predikce_tabulky.xlsx":{"url":"https://www.mfcr.cz/cs/rozpoctova-politika/makroekonomika/makroekonomicka-predikce",
                                    "xpath": ["(//a[contains(@class, 'b-') and contains(@href, 'makroekonomicka-predikce')]/@href)[1]"],
                                    "xpath_link":["//a[contains(@title, 'Tabulky-a-grafy')]/@href"]}
        }

        for name, value in urls.items():
                if value["xpath"]:
                    yield scrapy.Request(url=value["url"], callback=self.parse_xpath, dont_filter=True, cb_kwargs = {"name": name, "xpath": value["xpath"], "xpath_link": value["xpath_link"]})
                else:
                    yield scrapy.Request(url=value["url"], callback=self.parse_link, cb_kwargs={"name": name, "xpath_link": value["xpath_link"]})

    def parse_xpath(self, response: scrapy.http.response.Response, name: str, xpath: Generator | list[str], xpath_link: str) -> Generator[Any, Any, Any]:
            curr_xpath = xpath.pop(0) if xpath else None
            new_links = response.xpath(curr_xpath).getall() if curr_xpath else [response.url]
            for new_link in new_links:
                 if xpath:
                      yield scrapy.Request(url=response.urljoin(new_link), dont_filter=True, callback=self.parse_xpath, cb_kwargs={"name": name, "xpath": xpath, "xpath_link": xpath_link})
                 else:
                      yield scrapy.Request(url=response.urljoin(new_link), callback=self.parse_link, cb_kwargs={"name": name, "xpath_link": xpath_link})

    def parse_link(self, response: scrapy.http.response.Response, name: str, xpath_link: str) -> Generator[Any, Any, Any]:
        file_url = response.xpath(xpath_link[0]).get() if xpath_link else response.url
        file_url = response.urljoin(file_url)
        item = MacroScrapyItem()
        item["file_urls"] = [file_url]
        item["original_file_name"] = name
        yield item

