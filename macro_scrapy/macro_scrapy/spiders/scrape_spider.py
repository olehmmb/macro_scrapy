"""Spider for scraping macroeconomic files."""
from typing import Any, Generator

import scrapy
from macro_scrapy.items import MacroScrapyItem
from scrapy.http.response import Response


class GDPSpider(scrapy.Spider):
    """A Scrapy Spider class for scraping macroeconomic files.

    Attributes:
        name (str): The name of the spider.
    """

    name = 'files_spider'

    def start_requests(self) -> Generator[Any, Any, Any]:
        """Generate the initial requests to scrape the data.

        Yields:
            scrapy.Request: The request to be processed.
        """
        url = 'url'
        xpath = 'xpath'
        urls = {
            'GDP_Contributions.xlsx': {
                url: 'https://apl.czso.cz/pll/rocenka/rocenkavyber.kvart?mylang=CZ&j=Tab_GS',
                xpath: ['//a[text()="Stahnout vše v jednom souboru XLSX"]/@href'],
                },
            'GDP_Expenses.xlsx': {
                url: 'https://apl.czso.cz/pll/rocenka/rocenkavyber.kvart?mylang=CZ&j=Tab_VS',
                xpath: ['//a[text()="Stahnout vše v jednom souboru XLSX"]/@href'],
                },
            'GDP_Sources.xlsx': {
                url: 'https://apl.czso.cz/pll/rocenka/rocenkavyber.kvart?mylang=CZ&j=Tab_ZS',
                xpath: ['//a[text()="Stahnout vše v jednom souboru XLSX"]/@href'],
                },
            'Electricity.zip': {
                url: 'https://www.ote-cr.cz/cs/statistika/rocni-zprava?date=%7Bstr(currentYear-1)%7D-01-01',
                xpath: ['//a[contains(text(),"Rocni_zprava_o_trhu_2024_V0.zip")]/@href'],
                },
            'Gas.zip': {
                url: 'https://www.ote-cr.cz/cs/statistika/rocni-zprava?date=%7Bstr(currentYear-1)%7D-01-01',
                xpath: ['//a[contains(text(), "Rocni_zprava_o_trhu_2024_V0_plyn.zip")]/@href'],
                },
            'Unemployment.zip': {
                url: 'https://www.mpsv.cz/web/cz/mesicni',
                xpath: ['//a[@class="download-icon"]/@href'],
                },
            'ForeignTrade_M.xlsx': {
                url: 'https://vdb.czso.cz/vdbvo2/faces/cs/xlsexp?page=vystup-objekt&z=T&f=TABULKA&skupId=2848&katalog=32935&pvo=VZO011-NP-D&str=str(236)',
                xpath: [],
                },
            'ForeignTrade_Q.xlsx': {
                url: 'https://vdb.czso.cz/vdbvo2/faces/cs/xlsexp?page=vystup-objekt&z=T&f=TABULKA&skupId=2848&katalog=32935&pvo=VZO011-NP-C&str=str(395)',
                xpath: [],
                },
            'ForeignTrade_Y.xlsx': {
                url: 'https://vdb.czso.cz/vdbvo2/faces/cs/xlsexp?page=vystup-objekt&z=T&f=TABULKA&skupId=2848&katalog=32935&pvo=VZO011-NP-B&str=str(153)',
                xpath: [],
                },
            'CNB_Dluh_Struktura.xlsx': {
                url: 'https://www.cnb.cz/aradb/api/v13/file?lang=cs&trans=true&nameType=4&periodSorting=desc&periodFrom=817776000000&periodTo=1669852800000&setId=1086&setParams=&roleId=U&indList=SGFSDLUHSTRY200402W031,SGFSDLUHSTRY040402W031,SGFSDLUHSTRY050302W031,SGFSDLUHSTRY050202W031,SGFSDLUHSTRY070302W031,SGFSDLUHSTRY070202W031,SGFSDLUHSTRY200402W231,SGFSDLUHSTRY200404W231,SGFSDLUHSTRY200406W231,SGFSDLUHSTRY200405W231,SGFSDLUHSTRY200414W231,SGFSDLUHSTRY200402W131,SGFSDLUHSTRY200402I831,SGFSDLUHSTRY200402J831,SGFSDLUHSTRY200402W034,SGFSDLUHSTRY200402W036,SGFSDLUHSTRY200402W035,SGFSDLUHSTRY200302W031,SGFSDLUHSTRY200202W031,SGFSDLUHSTRY210202W031,SGFSDLUHSTRY200602W031,SGFSDLUHSTRY200802W031,SGFSDLUHSTRY210802W031,SGFSDLUHSTRY200902W031,SGFSDLUHSTRY210902W031,SGFSDLUHSTRY200702W031,SGFSDLUHSTRY060202W031,SGFSDLUHSTRY070404W031,SGFSDLUHSTRY200502W031,SGFSDLUHSTRY150402W031&id=1086&type=set&snList=&freqFilter=Y',
                xpath: [],
                },
            'REPO.xlsx': {
                url: 'https://www.cnb.cz/aradb/api/v13/file?lang=en&nameType=1&periodFrom=1210333000000&periodTo=1712317000000&indList=SFTP01M11',
                xpath: [],
                },
            'Households_Debt.csv': {
                url: 'https://stats.oecd.org/SDMX-JSON/data/NAAG/.DBTS14_S15NDI/OECD?contentType=csv',
                xpath: [],
                },
            "Households_DisposableIncome_Q.csv": {
                url:"https://stats.oecd.org/SDMX-JSON/data/DP_LIVE/CZE.HHDI.GROSS.PC_CHGPPCAP.Q/OECD?contentType=csv",
                xpath: [],
                },
            "Households_DisposableIncome_Y.csv": {
                url:"https://stats.oecd.org/SDMX-JSON/data/DP_LIVE/CZE.HHDI.GROSS.PC_CHGPPCAP.A/OECD?contentType=csv",
                xpath: [],
                },
            'IndustrialEvolution_M.xlsx': {
                url: 'https://www.czso.cz/csu/czso/pru_cr',
                xpath: ['//a[@class="out" and contains(@href, "xid=1725")]/@href'],
                },
            'IndustrialEvolution_Q.xlsx': {
                url: 'https://www.czso.cz/csu/czso/pru_cr',
                xpath: ['//a[@class="out" and contains(@href, "xid=1733")]/@href'],
                },
            'IndustrialEvolution_Y.xlsx': {
                url: 'https://www.czso.cz/csu/czso/pru_cr',
                xpath: ['//a[@class="out" and contains(@href, "xid=1801")]/@href'],
                },
            'IndustrialOrders_M.xlsx': {
                url: 'https://www.czso.cz/csu/czso/pru_cr',
                xpath: ['//a[@class="out" and contains(@href, "xid=1814")]/@href'],
                },
            'IndustrialOrders_Q.xlsx': {
                url: 'https://www.czso.cz/csu/czso/pru_cr',
                xpath: ['//a[@class="out" and contains(@href, "xid=1818")]/@href'],
                },
            'IndustrialOrders_Y.xlsx': {
                url: 'https://www.czso.cz/csu/czso/pru_cr',
                xpath: ['//a[@class="out" and contains(@href, "xid=1822")]/@href'],
                },
            'Retail_M.xlsx': {
                url: 'https://vdb.czso.cz/pll/eweb/vdb2xls.export?xid=730',
                xpath: [],
                },
            'Retail_Q.xlsx': {
                url: 'https://vdb.czso.cz/pll/eweb/vdb2xls.export?xid=761',
                xpath: [],
                },
            'Retail_Y.xlsx': {
                url: 'https://vdb.czso.cz/pll/eweb/vdb2xls.export?xid=769',
                xpath: [],
                },
            'CNB_macroindicators.xlsx': {
                url: 'https://www.cnb.cz/cs/menova-politika/prognoza/',
                xpath: ['//a[contains(text(), "indikátorů")]/@href'],
                },
            'Savings.xlsx': {
                url: 'https://www.czso.cz/documents/11350/191095591/csu010524_1.xlsx/a0a3e0bc-794f-4d20-b085-5d95d3505dba?version=1.0',
                xpath: [],
                },
            'Capacity.xlsx': {
                url: 'https://www.czso.cz/documents/11350/218351664/gkpr012424_4.xlsx/d2605378-9cc1-4cc9-b701-7e766cf29ebb?version=1.0',
                xpath: [],
                },
            'Sentiment.xlsx': {
                url: 'https://www.czso.cz/documents/11350/218351664/gkpr012424_5.xlsx/c4b9fb47-f5db-4b6a-9e1a-88f1c8efbdff?version=1.0',
                xpath: [],
                },
            'GrossWage.xlsx': {
                url: 'https://www.czso.cz/documents/11350/190537026/gpmz030524.xlsx/387a2ec7-c808-4915-9cdf-0720c82e21d5?version=1.0',
                xpath: [],
                },
            'MedianWage.xlsx': {
                url: 'https://www.czso.cz/documents/11350/122733562/pmz030821_5.xlsx/1b3900a3-0123-45ee-8c0c-524aca3851bf?version=1.0',
                xpath: [],
                },
        }

        yield from (
            scrapy.Request(
                url=target_value[url],
                callback=self.parse_link,
                dont_filter=True,
                cb_kwargs={'name': name, 'xpath': target_value[xpath]},
                )
            for name, target_value in urls.items()
        )

    def parse_link(self, response: Response, name: str, xpath: str) -> Generator[Any, Any, Any]:
        """Parse the response and yields the file to be downloaded.

        Args:
            response (Response): The response object to parse.
            name (str): The name of the file.
            xpath (str): The xpath to find the file URL.

        Yields:
            MacroScrapyItem: The item to be downloaded.
        """
        file_url = response.xpath(xpath[0]).get() if xpath else response.url
        file_url = response.urljoin(file_url)
        downloaded_file = MacroScrapyItem()
        downloaded_file['file_urls'] = [file_url]
        downloaded_file['original_file_name'] = name
        yield downloaded_file
