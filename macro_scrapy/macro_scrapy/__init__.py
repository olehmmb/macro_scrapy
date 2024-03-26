"""Project management package. The project is supposed to automize obtaining various macroeconomic indicators.

This package provides resources for the project as a whole.
It introduces variables that are subsequently used for manipulation with the files and folders.
"""

from datetime import datetime as dt
from datetime import timezone

parent_folder = r"C:\Users\212627578\PythonProjects\macro_scrapy"
current_date = dt.now(tz=timezone.utc)
folder_name = current_date.strftime("%Y%m%d")
