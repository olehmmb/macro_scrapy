"""Main module for processing 2W CNB repo data."""
import polars as pl
from __init__ import ExcelHandler, input_path, output_path


class EurCzkData:
    """A class to process EUR/CZK exchange rates from a .csv file."""

    def __init__(self):
        """Initialize EurCzkData with necessary attributes."""
        self.input_file = '{0}CNB_EUR_CZK.csv'.format(input_path)
        self.output_file = '{0}Eur_Czk.xlsx'.format(output_path)
        self.excel_handler = ExcelHandler()

    def melt_dataframe_into_long_format(self) -> 'EurCzkData':
        """
        Melt the dataframe into a long format.

        Melt the dataframe into a long format.

        Returns:
            EurCzkData: An instance of the EurCzkData class.
        """
        self.excel_handler.df = self.excel_handler.df.melt(
            id_vars='year',
            value_vars=pl.selectors.by_dtype([pl.Float64]),
            variable_name='month',
            value_name='eur_czk',
            )
        return self

    def run_it_all(self):
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
            null_values='\xa0',
        )
        self.melt_dataframe_into_long_format()
        self.excel_handler.write_data(output_file=self.output_file)


if __name__ == '__main__':
    EurCzkData().run_it_all()
