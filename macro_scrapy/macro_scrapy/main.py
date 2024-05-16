"""Module with functions to create folders for data and run Scrapy spiders."""
from pathlib import Path

from __init__ import folder_name, parent_folder
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def create_folder() -> None:
    """Create folders for input/output data."""
    # Create a folder with current date as a name for scraped data
    folder_path = '{0}/data/{1}'.format(parent_folder, folder_name)
    Path(folder_path).mkdir(parents=True, exist_ok=True)

    # Create input / output folders for clearer manipulation with the data
    subfolder1 = 'input'
    subfolder2 = 'output'
    Path(Path(folder_path) / subfolder1).mkdir(parents=True, exist_ok=True)
    Path(Path(folder_path) / subfolder2).mkdir(parents=True, exist_ok=True)


def run_spiders() -> None:
    """Run multiple Scrapy spiders."""
    # Create CrawlerProcess and SpiderLoader
    process = CrawlerProcess(get_project_settings())
    process.crawl('inflation_spider')
    process.crawl('mfcr_spider')
    process.crawl('files_spider')
    process.crawl('tables_spider')
    process.crawl('gov_debt')
    # Start crawling
    process.start()


if __name__ == '__main__':
    create_folder()
    run_spiders()
