"""Processing management package.

This package provides resources for processing.
It introduces variables that are subsequently used for obtaining / storing raw and processed data.
"""

from datetime import datetime as dt
from datetime import timezone

parent_folder = r"C:\Users\212627578\PythonProjects\macro_scrapy"
current_date = dt.now(tz=timezone.utc)
folder_name = current_date.strftime("%Y%m%d")
