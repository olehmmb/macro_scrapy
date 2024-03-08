import scrapy

from macro_scrapy.items import MacroScrapyItem


class GDPSpider(scrapy.Spider):
    name = "gdp"

    def start_requests(self):
        urls = [
            "https://apl.czso.cz/pll/rocenka/rocenkavyber.kvart?mylang=CZ&j=Tab_GS",
            "https://apl.czso.cz/pll/rocenka/rocenkavyber.kvart?mylang=CZ&j=Tab_VS",
            "https://apl.czso.cz/pll/rocenka/rocenkavyber.kvart?mylang=CZ&j=Tab_ZS"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        file_title = file_url = response.xpath("//a[text()='Stahnout vše v jednom souboru XLSX']/@title").get()
        file_url = response.xpath("//a[text()='Stahnout vše v jednom souboru XLSX']/@href").get()
        file_url = response.urljoin(file_url)
        item = MacroScrapyItem()
        item["file_urls"] = [file_url]
        item["original_file_name"] = [file_title]
        yield item
