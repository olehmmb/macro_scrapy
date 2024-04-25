from pathlib import Path

from __init__ import folder_name, parent_folder
from scrapy import spiderloader
from scrapy.crawler import CrawlerProcess
from scrapy.utils import project


def create_folder() -> None:

    # Create a folder with current date as a name, where the scraped data will be stored
    folder_path = fr"{parent_folder}/data/{folder_name}"
    Path(folder_path).mkdir( exist_ok=True)

    # Create input / output folders for clearer manipulation with the data
    subfolder1 = "input"
    subfolder2 = "output"
    Path(Path(folder_path) / subfolder1).mkdir(parents=True, exist_ok=True)
    Path(Path(folder_path) / subfolder2).mkdir(parents=True, exist_ok=True)

def run_spiders() -> None:

    settings = project.get_project_settings()

    # Create CrawlerProcess and SpiderLoader
    process = CrawlerProcess(settings)
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)

    # List all spiders you would like to run
    spider_names = ["files_spider"]

    for spider_name in spider_names:
        # Retrieve spider by name
        spider_cls = spider_loader.load(spider_name)

        # Add spider to the process
        process.crawl(spider_cls)

    # Start crawling
    process.start()

if __name__ == "__main__":
    create_folder()
    run_spiders()
