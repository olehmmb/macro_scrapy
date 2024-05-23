"""Output for Household Debt calculation."""
from datetime import date

import polars as pl
from __init__ import ExcelHandler, input_path, output_path


class HouseholdDebt:
    """A class to handle the processing of Households Debt data."""

    def __init__(self) -> None:
        """Initialize the Household Debt class."""
        self.input_file = '{0}Households_Debt.csv'.format(
            input_path,
            )
        self.output_file = '{0}Households_Debt.xlsx'.format(
            output_path,
            )
        self.excel_handler = ExcelHandler()

    def process_data(self) -> 'HouseholdDebt':
        """
        Fitlering selected countries, creating a column showing data for V4.

        Returns:
            HouseholdDebt: An instance of the HouseholdDebt class.
        """
        df = self.excel_handler.df
        countries = [
            ('POL', 'pl'),
            ('HUN', 'hu'),
            ('SVK', 'sk'),
            ('CZE', 'cz'),
            ('DEU', 'de'),
            ]

        series_dict = {
            series_name: (
                df.filter(pl.col('LOCATION') == country)[['Value']].rename(
                    {'Value': series_name},
                    )
            )
            for country, series_name in countries
        }

        df = pl.concat(list(series_dict.values()), how='horizontal')
        df = df.with_columns(
            v4=(pl.col('pl')+pl.col('hu')+pl.col('sk'))/3,
            )

        self.excel_handler.df = df
        return self

    def add_date_column(self) -> 'HouseholdDebt':
        """
        Add date column to DataFrame based on start_date.

        Returns:
            UnemploymentData: An instance of the UnemploymentData class.
        """
        df = self.excel_handler.df
        df = df.with_columns(time=pl.date_range(
            start=date(1995, 12, 31),
            end=date(1995+len(df)-1, 12, 31),
            interval='1y',
            ),
                )

        self.excel_handler.df = df
        return self

    def run_it_all(self):
        """Execute all the steps to process the retail data."""
        self.excel_handler.read_data_csv(
            source=self.input_file,
            has_header=True,
            )
        self.process_data().add_date_column()
        self.excel_handler.write_data(output_file=self.output_file)


if __name__ == '__main__':
    HouseholdDebt().run_it_all()
