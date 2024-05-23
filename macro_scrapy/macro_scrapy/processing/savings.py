"""Output for Savings calculation."""
import polars as pl
from __init__ import ExcelHandler, input_path, output_path


class Savings:
    """A class to handle the processing of Savings data."""

    def __init__(self) -> None:
        """Initialize the Savings class."""
        self.input_file = '{0}Savings.xlsx'.format(
            input_path,
            )
        self.output_file = '{0}SavingRate.xlsx'.format(
            output_path,
            )
        self.excel_handler = ExcelHandler()

    def process_data(self) -> 'Savings':
        """Process the data.

        Set column names and forward fill 'Year' values.

        Returns:
            Capacity: An instance of the Capacity class.
        """
        self.excel_handler.df.columns = [
            'Year', 'Quartal', 'Saving Rate', 'Investment Rate',
            ]
        self.excel_handler.df.with_columns(pl.col('Year').forward_fill())
        return self

    def run_it_all(self):
        """Execute all the steps to process the savings data."""
        self.excel_handler.read_data(
            excel_stream=self.input_file,
            skip_rows=7,
            sheet_name='List1',
            has_header=False,
            columns=[1, 2, 5, 6],
            )
        self.process_data()
        self.excel_handler.write_data(output_file=self.output_file)


if __name__ == '__main__':
    Savings().run_it_all()
