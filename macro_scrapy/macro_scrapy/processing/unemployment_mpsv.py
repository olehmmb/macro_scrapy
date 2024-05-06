"""Main module for processing unemployment data."""
from datetime import date

import polars as pl
from __init__ import ExcelHandler, input_path, output_path


class UnemploymentData:
    """A class to process unemployment data from an Excel file within a zip."""

    def __init__(self):
        """Initialize UnemploymentData with necessary attributes."""
        self.start_date = date(1991, 1, 31)
        self.output_file = '{0}UnemployedVacancies.xlsx'.format(output_path)
        self.input_file = '{0}Unemployment.zip'.format(input_path)
        self.pattern = r'^2\. Nez.*\.xlsx$'
        self.excel_handler = ExcelHandler()

    def process_data(self) -> 'UnemploymentData':
        """
        Process data by transposing and taking first two rows.

        Returns:
            UnemploymentData: An instance of the UnemploymentData class.
        """
        self.excel_handler.df = self.excel_handler.df.head(2)
        self.excel_handler.df = self.excel_handler.df.transpose(
            column_names='column_1',
            )
        return self

    def add_date_column(self) -> 'UnemploymentData':
        """
        Add date column to DataFrame based on start_date.

        Returns:
            UnemploymentData: An instance of the UnemploymentData class.
        """
        df_length = self.excel_handler.df.shape[0] - 1
        self.excel_handler.df = self.excel_handler.df.with_columns(
            date=pl.date_range(
                self.start_date,
                pl.Series([self.start_date]).dt.offset_by(
                    '{0}mo'.format(df_length),
                    ),
                '1mo',
                eager=True,
            ),
        )
        return self

    def run_it_all(self):
        """
        Execute all the steps to process the unemployment data.

        This method performs the following steps:
        Finds the Excel file in the zip archiveExtracts the specified file.
        Reads the Excel file into a DataFrame and processes the data by
        transposing and taking the first two rows. Adds a date column to
        the DataFrame. Writes the DataFrame to an Excel file.
        """
        self.excel_handler.find_excel_file_in_zip(
            self.input_file, self.pattern,
            ).unzip_file()
        self.excel_handler.read_data(
            sheet_name='List1', skip_rows=1, has_header=False,
            )
        self.process_data().add_date_column()
        self.excel_handler.write_data(self.output_file)


if __name__ == '__main__':
    UnemploymentData().run_it_all()
