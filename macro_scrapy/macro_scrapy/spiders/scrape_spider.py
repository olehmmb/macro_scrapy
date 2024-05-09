from __future__ import annotations

from typing import Any, Generator

import scrapy

from macro_scrapy.items import MacroScrapyItem


class GDPSpider(scrapy.Spider):
    name = 'files_spider'

    def start_requests(self) -> Generator[Any, Any, Any]:
        urls = {
            'GDP_Contributions.xlsx': {'url': 'https://apl.czso.cz/pll/rocenka/rocenkavyber.kvart?mylang=CZ&j=Tab_GS',
                                       'xpath_link': ['//a[text()="Stahnout vše v jednom souboru XLSX"]/@href']},
            'GDP_Expenses.xlsx': {'url': 'https://apl.czso.cz/pll/rocenka/rocenkavyber.kvart?mylang=CZ&j=Tab_VS',
                                         'xpath_link': ['//a[text()="Stahnout vše v jednom souboru XLSX"]/@href']},
            'GDP_Sources.xlsx': {'url': 'https://apl.czso.cz/pll/rocenka/rocenkavyber.kvart?mylang=CZ&j=Tab_ZS',
                                        'xpath_link': ['//a[text()="Stahnout vše v jednom souboru XLSX"]/@href']},
            'Electricity.zip': {'url': 'https://www.ote-cr.cz/cs/statistika/rocni-zprava?date=%7Bstr(currentYear-1)%7D-01-01',
                                       'xpath_link': ['//a[contains(text(),"Rocni_zprava_o_trhu_2024_V0.zip")]/@href']},
            'Gas.zip': {'url': 'https://www.ote-cr.cz/cs/statistika/rocni-zprava?date=%7Bstr(currentYear-1)%7D-01-01',
                               'xpath_link': ['//a[contains(text(), "Rocni_zprava_o_trhu_2024_V0_plyn.zip")]/@href']},
            'Unemployment.zip': {'url': 'https://www.mpsv.cz/web/cz/mesicni',
                                        'xpath_link': ['//a[@class="download-icon"]/@href']},
            'ForeignTrade_M.xlsx': {'url': 'https://vdb.czso.cz/vdbvo2/faces/cs/xlsexp?page=vystup-objekt&z=T&f=TABULKA&skupId=2848&katalog=32935&pvo=VZO011-NP-D&str=str(236)',
                                           'xpath_link': []},
            'ForeignTrade_Q.xlsx': {'url': 'https://vdb.czso.cz/vdbvo2/faces/cs/xlsexp?page=vystup-objekt&z=T&f=TABULKA&skupId=2848&katalog=32935&pvo=VZO011-NP-C&str=str(395)',
                                    'xpath_link': []},
            'ForeignTrade_Y.xlsx': {'url': 'https://vdb.czso.cz/vdbvo2/faces/cs/xlsexp?page=vystup-objekt&z=T&f=TABULKA&skupId=2848&katalog=32935&pvo=VZO011-NP-B&str=str(153)',
                                    'xpath_link': []},
            'CNB_Dluh_Struktura.xlsx': {'url': 'https://www.cnb.cz/aradb/api/v13/file?lang=cs&trans=true&nameType=4&periodSorting=desc&periodFrom=817776000000&periodTo=1669852800000&setId=1086&setParams=&roleId=U&indList=SGFSDLUHSTRY200402W031,SGFSDLUHSTRY040402W031,SGFSDLUHSTRY050302W031,SGFSDLUHSTRY050202W031,SGFSDLUHSTRY070302W031,SGFSDLUHSTRY070202W031,SGFSDLUHSTRY200402W231,SGFSDLUHSTRY200404W231,SGFSDLUHSTRY200406W231,SGFSDLUHSTRY200405W231,SGFSDLUHSTRY200414W231,SGFSDLUHSTRY200402W131,SGFSDLUHSTRY200402I831,SGFSDLUHSTRY200402J831,SGFSDLUHSTRY200402W034,SGFSDLUHSTRY200402W036,SGFSDLUHSTRY200402W035,SGFSDLUHSTRY200302W031,SGFSDLUHSTRY200202W031,SGFSDLUHSTRY210202W031,SGFSDLUHSTRY200602W031,SGFSDLUHSTRY200802W031,SGFSDLUHSTRY210802W031,SGFSDLUHSTRY200902W031,SGFSDLUHSTRY210902W031,SGFSDLUHSTRY200702W031,SGFSDLUHSTRY060202W031,SGFSDLUHSTRY070404W031,SGFSDLUHSTRY200502W031,SGFSDLUHSTRY150402W031&id=1086&type=set&snList=&freqFilter=Y',
                                               'xpath_link': []},
            'REPO.xlsx': {'url': 'https://www.cnb.cz/aradb/api/v13/file?lang=en&nameType=1&periodFrom=1210333000000&periodTo=1712317000000&indList=SFTP01M11',
                          'xpath_link': []},
            'Households_Debt.csv': {'url': 'https://stats.oecd.org/SDMX-JSON/data/NAAG/.DBTS14_S15NDI/OECD?contentType=csv',
                                    'xpath_link': []},
            'Households_DisposableIncome.csv': {'url': 'https://stats.oecd.org/SDMX-JSON/data/DP_LIVE/CZE.HHDI.GROSS.PC_CHGPPCAP.Q/OECD?contentType=csv',
                                                'xpath_link': []},
            'IndustrialEvolution_M.xlsx': {'url': 'https://www.czso.cz/csu/czso/pru_cr',
                                           'xpath_link': ['//a[@class="out" and contains(@href, "xid=1725")]/@href']},
            'IndustrialEvolution_Q.xlsx': {'url': 'https://www.czso.cz/csu/czso/pru_cr',
                                           'xpath_link': ['//a[@class="out" and contains(@href, "xid=1733")]/@href']},
            'IndustrialEvolution_Y.xlsx': {'url': 'https://www.czso.cz/csu/czso/pru_cr',
                                           'xpath_link': ['//a[@class="out" and contains(@href, "xid=1801")]/@href']},
            'IndustrialOrders_M.xlsx': {'url': 'https://www.czso.cz/csu/czso/pru_cr',
                                        'xpath_link': ['//a[@class="out" and contains(@href, "xid=1814")]/@href']},
            'IndustrialOrders_Q.xlsx': {'url': 'https://www.czso.cz/csu/czso/pru_cr',
                                        'xpath_link': ['//a[@class="out" and contains(@href, "xid=1818")]/@href']},
            'IndustrialOrders_Y.xlsx': {'url': 'https://www.czso.cz/csu/czso/pru_cr',
                                        'xpath_link': ['//a[@class="out" and contains(@href, "xid=1822")]/@href']},
            'Retail_M.xlsx': {'url': 'https://vdb.czso.cz/pll/eweb/vdb2xls.export?xid=730',
                              'xpath_link': []},
            'Retail_Q.xlsx': {'url': 'https://vdb.czso.cz/pll/eweb/vdb2xls.export?xid=761',
                              'xpath_link': []},
            'Retail_Y.xlsx': {'url': 'https://vdb.czso.cz/pll/eweb/vdb2xls.export?xid=769',
                              'xpath_link': []},
            'CNB_macroindicators.xlsx': {'url': 'https://www.cnb.cz/cs/menova-politika/prognoza/',
                                         'xpath_link': ['//a[contains(text(), "indikátorů")]/@href']},
            'Savings.xlsx': {'url': 'https://www.czso.cz/documents/11350/191095591/csu010524_1.xlsx/a0a3e0bc-794f-4d20-b085-5d95d3505dba?version=1.0',
                                    'xpath_link': []},
            'Sentiment.xlsx': {'url': 'https://www.czso.cz/documents/11350/218351664/gkpr012424_5.xlsx/c4b9fb47-f5db-4b6a-9e1a-88f1c8efbdff?version=1.0',
                               'xpath_link': []},
            'GrossWage.xlsx': {'url': 'https://www.czso.cz/documents/11350/190537026/gpmz030524.xlsx/387a2ec7-c808-4915-9cdf-0720c82e21d5?version=1.0',
                               'xpath_link': []},
            'MedianWage.xlsx': {'url': 'https://www.czso.cz/documents/11350/122733562/pmz030821_5.xlsx/1b3900a3-0123-45ee-8c0c-524aca3851bf?version=1.0',
                                'xpath_link': []},
        }

        for name, value in urls.items():
            yield scrapy.Request(url=value['url'], callback=self.parse_link, cb_kwargs={'name': name, 'xpath_link': value['xpath_link']})

    def parse_link(self, response: scrapy.http.response.Response, name: str, xpath_link: str) -> Generator[Any, Any, Any]:
        file_url = response.xpath(xpath_link[0]).get() if xpath_link else response.url
        file_url = response.urljoin(file_url)
        item = MacroScrapyItem()
        item['file_urls'] = [file_url]
        item['original_file_name'] = [name]
        yield item
