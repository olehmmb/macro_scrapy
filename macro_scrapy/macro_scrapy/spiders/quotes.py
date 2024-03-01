from typing import Iterable
import os
import scrapy
from scrapy.http import Request
from macro_scrapy.items import QuoteItem
from scrapy_playwright.page import PageMethod


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    # allowed_domains = ['quotes.toscrape.com']
    # start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "proxy": {
                "server": os.environ.get("server"),
                "username": os.environ.get("username"),
                "password": os.environ.get("password"),
            },
        }
    }

    def start_requests(self):
        url ="http://quotes.toscrape.com/scroll"
        yield scrapy.Request(url, meta=dict(
            playwright= True,
            playwright_include_page= True,
            playwright_page_methods= [
                PageMethod("wait_for_selector", "div.quote"),
                # PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                # PageMethod("waitForSelector", "div.quote:nth-child(11)"), # 10 page

            ],
            errBack=self.handle_failure
        ))

    async def parse(self, response):
        page = response.meta["playwright_page"]
        screeshot= await page.screenshot(path="screenshot.png", full_page=True)
        await page.close()



        # for quote in response.css("div.quote"):
        #     quote_item = QuoteItem()
        #     quote_item["text"] = quote.css("span.text::text").get()
        #     quote_item["author"] = quote.css("span small.author::text").get()
        #     quote_item["tags"] = quote.css("div.tags a.tag::text").getall()
        #     yield quote_item

        # next_page = response.css(".next a::attr(href)").get()
        # if next_page is not None:
        #     next_page_url = "http://quotes.toscrape.com" + next_page
        #     yield response.follow(next_page_url, meta=dict(
        #         playwright= True,
        #         playwright_include_page= True,
        #         playwright_page_methods= [
        #             PageMethod("waitForSelector", "div.quote")
        #         ],
        #         errBack=self.handle_failure
        #     ))
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