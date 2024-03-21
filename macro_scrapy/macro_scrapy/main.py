from datetime import datetime as dt
from datetime import timezone
from pathlib import Path

from scrapy import spiderloader
from scrapy.crawler import CrawlerProcess
from scrapy.utils import project


def create_folder() -> None:

    # Create a folder with current date as a name, where the scraped data will be stored
    current_date = dt.now(tz=timezone.utc)
    folder_name = current_date.strftime("%Y%m%d")
    folder_path = fr"C:\Users\212627578\PythonProjects\macro_scrapy\data\{folder_name}"
    Path.mkdir(folder_path, exist_ok=True)

    # Create input / output folders for clearer manipulation with the data
    parent_folder = fr"C:\Users\212627578\PythonProjects\macro_scrapy\data\{folder_name}"
    subfolder1 = "input"
    subfolder2 = "output"
    Path(Path(parent_folder) / subfolder1, exist_ok=True).mkdir(parents=True)
    Path(Path(parent_folder) / subfolder2, exist_ok=True).mkdir(parents=True)

def run_spiders() -> None:

    settings = project.get_project_settings()

    # Create CrawlerProcess and SpiderLoader
    process = CrawlerProcess(settings)
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)

    # List all spiders you would like to run
    spider_names = ["Electricity", "Gas", "Unemployment", "Foreign", "GDP", "Households"
                ,"IndOrd", "IndEvo", "Retail", "Savings", "Sentiment", "Wages", "Debt"]

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
