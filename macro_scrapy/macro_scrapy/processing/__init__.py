"""Processing management package.

This package provides resources for processing.
It introduces variables that are subsequently used.
"""
import contextlib
import zipfile
from datetime import datetime as dt
from datetime import timezone
from pathlib import Path

import polars as pl
import xlrd
from openpyxl import Workbook
from xls2xlsx import XLS2XLSX

parent_folder = r'/workspaces/macro_scrapy'
current_date = dt.now(tz=timezone.utc)
current_year = current_date.year
folder_name = current_date.strftime('%Y%m%d')
input_path = parent_folder+'/data/'+folder_name+'/input/'+folder_name+'_'
output_path = parent_folder+'/data/'+folder_name+'/output/'+folder_name+'_'
quarter_months = [0, 3, 6, 9]
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']
date_list = []


def monthly_data(years: int) -> list:
    for i in range(years, -1, -1):
        specific_year = str(current_year - i)
        for j in range(0, len(months), 3):
            date_list.extend(months[j:j+3])
            if j == quarter_months[0]:
                date_list.append('Q1')
            elif j == quarter_months[1]:
                date_list.append('Q2')
            elif j == quarter_months[2]:
                date_list.append('Q3')
            elif j == quarter_months[3]:
                date_list.append('Q4')
        date_list.append(specific_year)
    return date_list


def quarterly_data(years: int) -> list:
    for i in range(years, -1, -1):
        for j in range(0, len(months), 3):
            if j == quarter_months[0]:
                date_list.append('Q1')
            elif j == quarter_months[1]:
                date_list.append('Q2')
            elif j == quarter_months[2]:
                date_list.append('Q3')
            elif j == quarter_months[3]:
                date_list.append('Q4')
        specific_year = str(current_year - i)
        date_list.append(specific_year)
    return date_list


def yearly_data(years: int) -> list:
    for i in range(years, -1, -1):
        specific_year = str(current_year - i)
        date_list.append(specific_year)
    return date_list


def monthly_data_no_qy(years: int) -> list:
    for i in range(years, -1, -1):
        specific_year = str(current_year - i)
        for j in range(0, len(months), 3):
            date_list.extend(months[j:j+3])
        date_list.append(specific_year)
    return date_list


def convert_xls(file_to_convert: any) -> any:
    convertable = XLS2XLSX(file_to_convert)
    return convertable.to_xlsx()


def average_every_4(lst: any) -> list:
    new_list = []
    for i in range(0, len(lst), 4):
        group = lst[i:i+4]
        group_average = sum(group) / len(group)
        new_list.extend(group)
        new_list.append(group_average)
    return new_list


def combine_lists_monthly(m: list, q: list, y: list) -> list:
    final_list = []
    index_q = 0
    index_y = 0
    for i, item in enumerate(m):
        final_list.append(item)
        if (i + 1) % 3 == 0 and index_q < len(q):
            final_list.append(q[index_q])
            index_q += 1
        if (i + 1) % 12 == 0 and index_y < len(y):
            final_list.append(y[index_y])
            index_y += 1
    return final_list


def row_selection(df_r: pl.DataFrame, row: int, column: any) -> any:
    df_r = df_r[row, column:]
    return df_r.transpose(include_header=False)


def column_selection(df_c: pl.DataFrame, row: any, column: int) -> pl.DataFrame:
    df_c = df_c[row:, column]
    return pl.DataFrame(df_c)


def list_growth(sequence: any) -> list:
    growth_list = []
    for i in sequence:
        growth = i-100
        growth_list.extend(growth)
    return growth_list


class ExcelHandler:
    """A class to handle Excel files"""

    def __init__(self):
        """Initialize ExcelHandler with necessary attributes."""
        self.excel_file_name = None
        self.excel_stream = None

    def find_excel_file_in_zip(self, input_file: str, file_regex: str):
        """
        Find the first Excel file in zip that matches a regular expression.

        Args:
            input_file (str): The input zip file.
            # file_regex (str): The regular expression to match the Excel file.

        Returns
        -------
            ExcelHandler: An instance of the ExcelHandler with the found Excel.
        """
        self.input_file = input_file
        self.file_regex = file_regex
        with ZipFile(self.input_file, 'r') as zip:
            for name in zip.namelist():
                if re.match(self.file_regex, name):
                    self.excel_file_name = name
                    break
        return self

    def unzip_file(self) -> 'ExcelHandler':
        """
        Extract specified file from zip archive.

        Returns
        -------
            ExcelHandler: An instance of the ExcelHandler class.
        """
        with ZipFile(self.input_file, 'r') as zip:
            self.excel_stream = zip.open(self.excel_file_name)
        return self

    def read_data(self, excel_stream=None, sheet_name='Sheet1', skip_rows=0,
                  has_header=True, columns=None, new_columns=None
                  ) -> 'ExcelHandler':
        """
        Read an Excel file into a DataFrame.

        Args:
            excel_stream (str, optional): The input Excel stream. Defaults to instance's excel_stream.
            sheet_name (str, optional): The name of the sheet to read from. Defaults to 'Sheet1'.
            skip_rows (int, optional): The number of rows to skip at the beginning. Defaults to 0.
            has_header (bool, optional): Whether the Excel file has a header. Defaults to True.
            columns (list, optional): The list of column names to consider. If not provided, all columns are considered.
            new_columns (list, optional): The list of renamed (new) columns to be assigned instead of the original ones.

        Returns
        -------
            ExcelHandler: An instance of the ExcelHandler class with the DataFrame read from the Excel file.
        """
        if excel_stream is None:
            excel_stream = self.excel_stream
        self.df = pl.read_excel(
            excel_stream,
            sheet_name=sheet_name,
            read_options={'skip_rows': skip_rows, 'has_header': has_header,
                          'columns': columns, 'new_columns': new_columns
                          },
        )
        return self

    def write_data(self, output_file: str) -> 'ExcelHandler':
        """
        Write DataFrame to Excel file.

        Returns
        -------
            ExcelHandler: An instance of the ExcelHandler class.
        """
        self.df.write_excel(output_file)
        return self

class CsvHandler:
    """A class to handle Csv files."""

    def read_data(self, source, skip_rows=0,  # noqa: PLR0913
                    has_header=False, separator=',',
                    encoding='utf8', missing_utf8_is_empty_string=False
                  ) -> 'CsvHandler':
        """
        Read an Csv file into a DataFrame.

        Args:
            source (str, optional): The input .csv file.
            skip_rows (int, optional): The number of rows to skip at the beginning. Defaults to 0.
            has_header (bool, optional): Whether the .csv file has a header. Defaults to True.
            encoding (str, optional): encoding of the .csv file. Defaults to 'utf8'
            missing_utf8_is_empty_string (bool, optional): whether to treat missing utf8 values as empty strings. Defaults to False.

        Returns
        -------
            CsvHandler: An instance of the CsvHandler class with the DataFrame read from the .csv file.
        """
        if source is None:
            source = self.source
        self.df = pl.scan_csv(
            source, has_header=has_header,
            separator=separator, encoding=encoding,
            missing_utf8_is_empty_string=missing_utf8_is_empty_string,
            skip_rows=skip_rows
        ).collect()
        return self

    def write_data(self, output_file: str) -> 'CsvHandler':
        """
        Write DataFrame to Excel file.

        Returns
        -------
            ExcelHandler: An instance of the CsvHandler class.
        """
        self.df.write_excel(output_file)
        return self
