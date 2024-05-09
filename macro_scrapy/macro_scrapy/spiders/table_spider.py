from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Generator

import scrapy
from scrapy.utils.project import get_project_settings

from . import folder_name


class TableSpider(scrapy.Spider):
    name = "tables_spider"
    dont_retrieve_year = ("CNB_EUR_CZK", "czso_inflace")
    def start_requests(self) -> Generator[Any, Any, Any]:
        urls = {
            "MFCR_state_deficit" : {"url" : "https://www.mfcr.cz/cs/rozpoctova-politika/statni-rozpocet/plneni-statniho-rozpoctu",
                                        "xpath" : ["(//a[contains(@href, 'mesicni-pokladni-plneni')])[1]/@href",
                                                   "(//a[contains(@href, 'mesicni-pokladni-plneni') and count(@*) = 1])[position()  <= 7]/@href"],
                                        "xpath_table": ["(//tbody)[1]/tr"]},
            "CNB_EUR_CZK" : {"url" : "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/prumerne_mena.html?mena=EUR",
                                        "xpath": [],
                                        "xpath_table" : ["(//table)[1]/tr"]},
        }

        for name, value in urls.items():
                if value["xpath"]:
                    yield scrapy.Request(url=value["url"], callback=self.parse_xpath, dont_filter=True, cb_kwargs = {"name": name, "xpath": value["xpath"], "xpath_table": value["xpath_table"][0]})
                else:
                    yield scrapy.Request(url=value["url"], callback=self.parse_table, cb_kwargs={"name": name, "xpath_table": value["xpath_table"][0]})

    def parse_xpath(self, response: scrapy.http.response.Response, name: str, xpath: Generator | list[str], xpath_table: str) -> Generator[Any, Any, Any]:
            curr_xpath = xpath[0]
            xpath = xpath[1:]
            new_links = response.xpath(curr_xpath).getall()
            for new_link in new_links:
                 if xpath:
                      yield scrapy.Request(url=response.urljoin(new_link), dont_filter=True, callback=self.parse_xpath, cb_kwargs={"name": name, "xpath": xpath, "xpath_table": xpath_table})
                 else:
                      yield scrapy.Request(url=response.urljoin(new_link), callback=self.parse_table, cb_kwargs={"name": name, "xpath_table": xpath_table})


    def parse_table(self, response: scrapy.http.response.Response, name: str, xpath_table: str) -> None:
        all_current_rows = [row.xpath("./*//text()").getall() for row in response.xpath(xpath_table)]
        all_current_rows = [[item for item in inner_list if item != "\xa0"] for inner_list in all_current_rows]
        year = "_" + all_current_rows[1][-1][-4:] if name not in self.dont_retrieve_year else ""
        csv_filename =  folder_name + "_" + f"{name}{year}.csv"
        csv_path = Path(get_project_settings().get("FILES_STORE")) / csv_filename
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with Path(csv_path).open(mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(all_current_rows)
