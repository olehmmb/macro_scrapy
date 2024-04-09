from datetime import datetime as dt
from datetime import timedelta as td

import scrapy
from scrapy.utils.project import get_project_settings

from macro_scrapy.items import MacroScrapyItem


class CNBARADSpider(scrapy.Spider):
    name = "cnb_arad"
    allowed_domains = ["www.mfcr.cz"]

    arad_api = "https://www.cnb.cz/aradb/api/v13/file?"
    today = dt.now()
    epoch = dt(1970, 1, 1)
    periodTo = int(round((today - epoch).total_seconds()*1000, -6))
    periodFrom = int(round(((today - td(weeks=830)) - epoch).total_seconds()*1000, -6))
    # indList = ("SGFSDLUHSTRY200402W031", 'SGFSDLUHSTRY040402W031', 'SGFSDLUHSTRY050302W031', 'SGFSDLUHSTRY050202W031', 'SGFSDLUHSTRY070302W031', 'SGFSDLUHSTRY070202W031',
    #            'SGFSDLUHSTRY200402W231', 'SGFSDLUHSTRY200404W231', 'SGFSDLUHSTRY200406W231', 'SGFSDLUHSTRY200405W231', 'SGFSDLUHSTRY200414W231', 'SGFSDLUHSTRY200402W131',
    #            'SGFSDLUHSTRY200402I831', 'SGFSDLUHSTRY200402J831', 'SGFSDLUHSTRY200402W034', 'SGFSDLUHSTRY200402W036', 'SGFSDLUHSTRY200402W035', 'SGFSDLUHSTRY200302W031',
    #            'SGFSDLUHSTRY200202W031', 'SGFSDLUHSTRY210202W031', 'SGFSDLUHSTRY200602W031', 'SGFSDLUHSTRY200802W031', 'SGFSDLUHSTRY210802W031', 'SGFSDLUHSTRY200902W031',
    #            'SGFSDLUHSTRY210902W031', 'SGFSDLUHSTRY200702W031', 'SGFSDLUHSTRY060202W031', 'SGFSDLUHSTRY070404W031', 'SGFSDLUHSTRY200502W031', 'SGFSDLUHSTRY150402W031')
    # urls=[f'{arad_api}lang=cs&nameType=4&periodFrom={periodFrom}&periodTo={periodTo}&setId=1086&indList={",".join(indList)}&id=1086&type=set&freqFilter=Y']
    urls = ["https://www.cnb.cz/aradb/api/v13/file?lang=cs&trans=true&nameType=4&periodSorting=desc&periodFrom=817776000000&periodTo=1669852800000&setId=1086&setParams=&roleId=U&indList=SGFSDLUHSTRY200402W031,SGFSDLUHSTRY040402W031,SGFSDLUHSTRY050302W031,SGFSDLUHSTRY050202W031,SGFSDLUHSTRY070302W031,SGFSDLUHSTRY070202W031,SGFSDLUHSTRY200402W231,SGFSDLUHSTRY200404W231,SGFSDLUHSTRY200406W231,SGFSDLUHSTRY200405W231,SGFSDLUHSTRY200414W231,SGFSDLUHSTRY200402W131,SGFSDLUHSTRY200402I831,SGFSDLUHSTRY200402J831,SGFSDLUHSTRY200402W034,SGFSDLUHSTRY200402W036,SGFSDLUHSTRY200402W035,SGFSDLUHSTRY200302W031,SGFSDLUHSTRY200202W031,SGFSDLUHSTRY210202W031,SGFSDLUHSTRY200602W031,SGFSDLUHSTRY200802W031,SGFSDLUHSTRY210802W031,SGFSDLUHSTRY200902W031,SGFSDLUHSTRY210902W031,SGFSDLUHSTRY200702W031,SGFSDLUHSTRY060202W031,SGFSDLUHSTRY070404W031,SGFSDLUHSTRY200502W031,SGFSDLUHSTRY150402W031&id=1086&type=set&snList=&freqFilter=Y"]
    indListRepo = "SFTP01M11"
    urls.append(f"{arad_api}lang=en&nameType=1&periodFrom={periodFrom}&periodTo={periodTo}&indList={indListRepo}")

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url = url, callback=self.parse)

    def parse(self, response):
        if "SGFSDLUHSTRY200402W031" in response.url:
            file_title = "National_debt.xlsx"
        else:
            file_title = "REPO.xlsx"
        file_url = response.url
        item = MacroScrapyItem()
        item["file_urls"] = [file_url]
        item["original_file_name"] = [file_title]
        yield item