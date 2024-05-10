"""Main module for processing 2W CNB repo data."""
import datetime

import polars as pl
import polars.selectors as cs
from __init__ import ExcelHandler, input_path, output_path
from dateutil.relativedelta import relativedelta


class EurCzkData:
    """A class to process EUR/CZK exchange rates from a .excel file."""

    def __init__(self):
        """Initialize EurCzkData with necessary attributes."""
        self.input_file = '{0}CNB_EUR_CZK.csv'.format(input_path)
        self.output_file = '{0}Eur_Czk.xlsx'.format(output_path)
        self.excel_handler = ExcelHandler()

    def replace_comma_with_a_dot(self) -> 'EurCzkData':
        """ 
        Replace decimal comma with decimal dot for all columns excluding
        "rok" column.

        :returns
            EurCzkData: An instance of the EurCzkData class.
        """
        self.excel_handler.df = (self.excel_handler.df
                                    .with_columns(pl.all().exclude("rok")
                                    .str.replace(",", ".")
                                    .cast(pl.Float32, strict=False)
                                    .round(3))
        )
        return self
    def rename_columns(self) -> 'EurCzkData':
        """
        Rename columns using integers from 00 to 12 indicating the corresponding month.

        Note that columns are arranged in an ascending order from left to right (January, February ...) in the .excel file.

        This transformation is needed in order to create "date" column of Datetime data type.

        Returns
        -------
            EurCzkData: An instance of the EurCzkData class.
        """
        self.excel_handler.df.columns = ["year"] + [str(i).zfill(2) for i in range(1, 13)]

        return self

    def melt_dataframe_into_long_format(self) -> 'EurCzkData':
        """
        Melt the dataframe into a long format. Concatenate "year" and newly created "variable" columns into "date" column and recast it from String to Datetime data type.

        Remove the newly created column "variable" indicating the original column names (00 -- 12).

        Returns.
        -------
            EurCzkData: An instance of the EurCzkData class.
        """
        self.excel_handler.df = self.excel_handler.df.melt(id_vars="year", value_vars = cs.by_dtype([pl.Float32]))
        self.excel_handler.df = ((self.excel_handler.df.with_columns(
                pl.concat_str([pl.col("year"), pl.col("variable")], separator="-")
                .map_elements(lambda x: (datetime.datetime.strptime(x, "%Y-%m") + relativedelta(months=1, days=-1)).replace(tzinfo=datetime.timezone.utc)).alias("date"))  # noqa: DTZ007
                )
                .drop("variable")
        )
        return self

    def sort_and_rename(self) -> 'EurCzkData':
        """
        Sort and rearrange the dataframe and rename "value" column to "eur_czk".

        Returns
        -------
            EurCzkData: An instance of the EurCzkData class.
        """
        self.excel_handler.df = (self.excel_handler.df.sort(pl.col("date"), descending=False)
            .rename({"value": "eur_czk"})
            .select("date", "year", "eur_czk")
        )

        return self

    def run_it_all(self):  # noqa: ANN201
        """
        Execute all the steps to process the CNB_EUR_CZK data.

        This method performs the following steps:
        Replaces decimal comma with decimal dot.
        Renames columns as integers.
        Melts the dataframe into a long format.
        Temporally sorts the final dataframe.
        Writes the DataFrame to an Excel file.
        """
        self.excel_handler.read_data_csv(
            source=self.input_file,
            has_header=True,
            encoding='utf8-lossy',
            missing_utf8_is_empty_string=True,
            )
        (self.replace_comma_with_a_dot()
            .rename_columns()
            .melt_dataframe_into_long_format()
            .sort_and_rename()
        )
        self.excel_handler.write_data(output_file=self.output_file)

if __name__ == '__main__':
    EurCzkData().run_it_all()
