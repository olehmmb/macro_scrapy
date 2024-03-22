from typing import Any, Generator

import scrapy

from macro_scrapy.items import MacroScrapyItem


class GDPSpider(scrapy.Spider):
    name = "spider"

    def start_requests(self) -> Generator[Any, Any, Any]:
        urls = {
            "GDP_Contributions.xlsx" : {"url" : "https://apl.czso.cz/pll/rocenka/rocenkavyber.kvart?mylang=CZ&j=Tab_GS",
                                        "xpath" : "//a[text()='Stahnout vše v jednom souboru XLSX']/@href"},
            "GDP_Expenses.xlsx" : {"url" : "https://apl.czso.cz/pll/rocenka/rocenkavyber.kvart?mylang=CZ&j=Tab_VS",
                                   "xpath" : "//a[text()='Stahnout vše v jednom souboru XLSX']/@href"},
            "GDP_Sources.xlsx" : {"url" : "https://apl.czso.cz/pll/rocenka/rocenkavyber.kvart?mylang=CZ&j=Tab_ZS",
                                  "xpath" : "//a[text()='Stahnout vše v jednom souboru XLSX']/@href"},
            "Electricity.zip":{"url":"https://www.ote-cr.cz/cs/statistika/rocni-zprava?date=%7Bstr(currentYear-1)%7D-01-01",
                               "xpath":"//a[contains(text(),'Rocni_zprava_o_trhu_2024_V0.zip')]/@href"},
            "Gas.zip":{"url":"https://www.ote-cr.cz/cs/statistika/rocni-zprava?date=%7Bstr(currentYear-1)%7D-01-01",
                               "xpath":"//a[contains(text(), 'Rocni_zprava_o_trhu_2024_V0_plyn.zip')]/@href"},
            "Unemployment.zip":{"url":"https://www.mpsv.cz/web/cz/mesicni",
                                "xpath":"//a[@class='download-icon']/@href"},
            "ForeignTrade_M.xlsx":{"url":"https://vdb.czso.cz/vdbvo2/faces/cs/xlsexp?page=vystup-objekt&z=T&f=TABULKA&skupId=2848&katalog=32935&pvo=VZO011-NP-D&str=str(236)",
                                   "xpath":""},
            "ForeignTrade_Q.xlsx":{"url":"https://vdb.czso.cz/vdbvo2/faces/cs/xlsexp?page=vystup-objekt&z=T&f=TABULKA&skupId=2848&katalog=32935&pvo=VZO011-NP-C&str=str(395)",
                                   "xpath":""},
            "ForeignTrade_Y.xlsx":{"url":"https://vdb.czso.cz/vdbvo2/faces/cs/xlsexp?page=vystup-objekt&z=T&f=TABULKA&skupId=2848&katalog=32935&pvo=VZO011-NP-B&str=str(153)",
                                   "xpath":""},
            "Dluh_Struktura.xlsx":{"url":"https://www.cnb.cz/aradb/api/v13/file?lang=cs&trans=true&nameType=4&periodSorting=desc&periodFrom=817776000000&periodTo=1669852800000&setId=1086&setParams=&roleId=U&indList=SGFSDLUHSTRY200402W031,SGFSDLUHSTRY040402W031,SGFSDLUHSTRY050302W031,SGFSDLUHSTRY050202W031,SGFSDLUHSTRY070302W031,SGFSDLUHSTRY070202W031,SGFSDLUHSTRY200402W231,SGFSDLUHSTRY200404W231,SGFSDLUHSTRY200406W231,SGFSDLUHSTRY200405W231,SGFSDLUHSTRY200414W231,SGFSDLUHSTRY200402W131,SGFSDLUHSTRY200402I831,SGFSDLUHSTRY200402J831,SGFSDLUHSTRY200402W034,SGFSDLUHSTRY200402W036,SGFSDLUHSTRY200402W035,SGFSDLUHSTRY200302W031,SGFSDLUHSTRY200202W031,SGFSDLUHSTRY210202W031,SGFSDLUHSTRY200602W031,SGFSDLUHSTRY200802W031,SGFSDLUHSTRY210802W031,SGFSDLUHSTRY200902W031,SGFSDLUHSTRY210902W031,SGFSDLUHSTRY200702W031,SGFSDLUHSTRY060202W031,SGFSDLUHSTRY070404W031,SGFSDLUHSTRY200502W031,SGFSDLUHSTRY150402W031&id=1086&type=set&snList=&freqFilter=Y",
                                   "xpath":""},

        }
        for name, value in urls.items():
            yield scrapy.Request(url=value["url"],callback=self.parse,cb_kwargs = {"name":name, "xpath":value["xpath"]})

    def parse(self, response: str, name: str, xpath: str) -> Generator[Any, Any, Any]:
        file_url = response.xpath(xpath).get() if xpath != "" else response.url
        file_url = response.urljoin(file_url)
        item = MacroScrapyItem()
        item["file_urls"] = [file_url]
        item["original_file_name"] = [name]
        yield item
