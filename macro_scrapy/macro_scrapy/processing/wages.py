"""Output for Wages calculation."""
import polars as pl
from __init__ import ExcelHandler, input_path, output_path


class Wages:
    """A class to handle the processing of Capacity data."""

    def __init__(self) -> None:
        """Initialize the EmployeePotential class."""
        self.input_file = '{0}GrossWage.xlsx'.format(
            input_path,
            )
        self.output_file = '{0}Wages.xlsx'.format(
            output_path,
            )
        self.excel_handler = ExcelHandler()

    def process_data(self) -> 'Wages':
        """Process the data.

        Drop the blank columns, transpose and forward fill 'Year' values.

        Returns:
        Wages: An instance of the Wages class.
        """
        df = self.excel_handler.df
        df = df.select(pl.exclude('column_1', 'column_2'))
        df = df.head(6)

        df = df.transpose(
            column_names=[
                'Year',
                'Quartal',
                'Average Wage',
                'Wage Growth',
                'Real Wage Growth',
                'Nominal Wage (adjusted)',
            ],
        )

        df.with_columns(pl.col('Year').forward_fill())
        self.excel_handler.df = df

    def run_it_all(self):
        """Execute all the steps to process the unemployment data."""
        self.excel_handler.read_data(
            excel_stream=self.input_file,
            sheet_name='Data',
            has_header=False,
            )
        self.process_data()
        self.excel_handler.write_data(output_file=self.output_file)


if __name__ == '__main__':
    Wages().run_it_all()
