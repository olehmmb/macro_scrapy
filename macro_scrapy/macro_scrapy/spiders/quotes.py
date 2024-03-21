from typing import Iterable
import os
import scrapy
from scrapy.http import Request
from macro_scrapy.items import QuoteItem
from scrapy_playwright.page import PageMethod

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
        'http://quotes.toscrape.com/page/1/'
    ]
    
    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                'text': quote.css("span.text::text").extract_first().replace("\u201c","").replace("\u201d",""),
                'author': quote.css("small.author::text").extract_first(),
                'tags': quote.css("div.tags a.tag::text").extract(),
            }
        


class QuotesScrollSpider(scrapy.Spider):
    name = 'quotesscroll'

    def start_requests(self):
        url ="http://quotes.toscrape.com/scroll"
        yield scrapy.Request(url, meta=dict(
            playwright= True,
            playwright_include_page= True,
            playwright_page_methods= [
                PageMethod("wait_for_selector", "div.quote"),
                PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                PageMethod("wait_for_selector", "div.quote:nth-child(15)"),
            ],
            errBack=self.handle_failure
        ))

    async def parse(self, response):
        page = response.meta["playwright_page"]
        screeshot= await page.screenshot(path="screenshot.png", full_page=True)
        await page.close()

    async def handle_failure(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

class QuotesJsSpider(scrapy.Spider):
    name = 'quotesjs'

    def start_requests(self):
        url ="https://quotes.toscrape.com/js/"
        yield scrapy.Request(url, meta=dict(
            playwright= True,
            playwright_include_page= True,
            playwright_page_methods= [
                PageMethod("wait_for_selector", "div.quote"),
            ],
            errBack=self.handle_failure
        ))

    async def parse(self, response):
        page = response.meta["playwright_page"]
        screeshot= await page.screenshot(path="screenshot.png", full_page=True)
        await page.close()



        for quote in response.css("div.quote"):
            quote_item = QuoteItem()
            quote_item["text"] = quote.css("span.text::text").get()
            quote_item["author"] = quote.css("span small.author::text").get()
            quote_item["tags"] = quote.css("div.tags a.tag::text").getall()
            yield quote_item

        next_page = response.css(".next a::attr(href)").get()
        if next_page is not None:
            next_page_url = "http://quotes.toscrape.com" + next_page
            yield response.follow(next_page_url, meta=dict(
                playwright= True,
                playwright_include_page= True,
                playwright_page_methods= [
                    PageMethod("wait_for_selector", "div.quote")
                ],
                errBack=self.handle_failure
            ))
    async def handle_failure(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

        # if failure.check(TimeoutError):
        #     self.logger.error("Timeout error")
        # elif failure.check(NoSuchElementException):
        #     self.logger.error("Element not found")
        # else:
        #     self.logger.error(f"Unknown error: {failure.getTraceback()}")
        # yield None