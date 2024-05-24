"""Module with functions to create folders for data and run Scrapy spiders."""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from settings import INPUT_FOLDER, OUTPUT_FOLDER


def create_folder() -> None:
    """Create folders for input/output data."""
    INPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


def run_spiders() -> None:
    """Create CrawlerProcess and run multiple Scrapy spiders."""
    process = CrawlerProcess(get_project_settings())
    process.crawl('mfcr_spider')
    process.crawl('files_spider')
    process.crawl('tables_spider')
    process.crawl('gov_debt')
    # Start crawling
    process.start()


if __name__ == '__main__':
    create_folder()
    run_spiders()
