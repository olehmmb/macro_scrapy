"""Pipelines for scrapy spider defined in settings.py."""

from macro_scrapy.settings import CURRENT_DATE
from scrapy.pipelines.files import FilesPipeline


class MacroScrapyPipeline(FilesPipeline):
    """
    A pipeline class for handling scraped files.

    This class overwrites the file_path method of the FilesPipeline
      to rename the scraped files.
    """

    def file_path(
        self, request, item=None, response=None, info=None,  # noqa: WPS110
            ) -> str:
        """Overwrite the file_path method to rename the scraped file.

        Args:
            request: The request object used to download the file.
            item: A dictionary containing the original file name.
            response: The response object used to download the file.
            info: The info object used to download the file.

        Returns:
            str: File name in the format 'CURRENT_DATE_original_file_name'.
        """
        return '{0}_{1}'.format(
            CURRENT_DATE,
            item['original_file_name'],
            )
