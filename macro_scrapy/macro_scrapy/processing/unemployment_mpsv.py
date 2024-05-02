"""Main module for processing unemployment data."""
from datetime import date
from zipfile import ZipFile

import polars as pl
from __init__ import input_path, output_path


class UnemploymentData:
    """
    A class to process unemployment data from an Excel file within a zip.

    Attributes:
        start_date (date): Start date for the data series.
        input_zip (str): Input zip file name without extension.
        output_file (str): Output Excel file name without extension.
    """

    def __init__(self, start_date, input_zip, output_file):
        """
        Initialize UnemploymentData with necessary attributes.

        Parameters:
            start_date (date): Start date for the data series.
            input_zip (str): Input zip file name without extension.
            output_file (str): Output Excel file name without extension.
        """
        self.start_date = start_date
        self.input_zip_path = '{0}_{1}'.format(input_path, input_zip)
        self.output_file_path = '{0}_{1}'.format(output_path, output_file)

    def find_excel_file_in_zip(self):
        """
        Find first Excel file in zip matching '2. Nez' and ending with '.xlsx'.

        Returns:
            str: Name of found Excel file or None if no match.
        """
        # Find first file matching '2. Nez' and ending with '.xlsx'
        with ZipFile(self.input_zip_path, 'r') as zip_archive:
            for name in zip_archive.namelist():
                if name.startswith('2. Nez') and name.endswith('.xlsx'):
                    return name
        return None

    def unzip_file(self, excel_file_name):
        """
        Extract specified file from zip archive.

        Parameters:
            excel_file_name (str): File name to extract.

        Returns:
            ZipExtFile: Extracted file object.
        """
        with ZipFile(self.input_zip_path, 'r') as zip_archive:
            return zip_archive.open(excel_file_name)

    def read_excel_file(self, excel_stream):
        """
        Read Excel file into DataFrame.

        Parameters:
            excel_stream (ZipExtFile): Excel file to read.

        Returns:
            DataFrame: Data as DataFrame.
        """
        return pl.read_excel(
            excel_stream,
            sheet_name='List1',
            read_options={'skip_rows': 1, 'has_header': False},
        )

    def process_data(self, dataframe):
        """
        Process data by transposing and taking first two rows.

        Parameters:
            dataframe (DataFrame): Data to process.

        Returns:
            DataFrame: Processed data.
        """
        return dataframe.head(2).transpose(column_names='column_1')

    def add_date_column(self, dataframe):
        """
        Add date column to DataFrame based on start_date.

        Parameters:
            dataframe (DataFrame): Data to add date column to.

        Returns:
            DataFrame: Data with added date column.
        """
        df_length = dataframe.shape[0] - 1
        return dataframe.with_columns(
            date=pl.date_range(
                self.start_date,
                pl.Series([self.start_date]).dt.offset_by(
                    '{0}mo'.format(df_length),
                    ),
                '1mo',
                eager=True,
            ),
        )

    def write_data(self, dataframe):
        """
        Write DataFrame to Excel file.

        Parameters:
            dataframe (DataFrame): Data to write to Excel file.
        """
        dataframe.write_excel(self.output_file_path)


if __name__ == '__main__':
    series_start = date(1991, 1, 31)
    unemployment_data = UnemploymentData(
        start_date=series_start,
        input_zip='Unemployment.zip',
        output_file='UnemployedVacancies.xlsx',
    )
    excel_file_name = unemployment_data.find_excel_file_in_zip()
    excel_stream = unemployment_data.unzip_file(excel_file_name)
    raw_df = unemployment_data.read_excel_file(excel_stream)
    processed_df = unemployment_data.process_data(raw_df)
    dataframe_with_dates = unemployment_data.add_date_column(processed_df)
    unemployment_data.write_data(dataframe_with_dates)
