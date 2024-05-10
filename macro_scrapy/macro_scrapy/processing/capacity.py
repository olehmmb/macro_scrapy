"""Output for Capacity calculation."""
import polars as pl
from __init__ import ExcelHandler, input_path, output_path


class Capacity:
    """A class to handle the processing of Capacity data."""

    def __init__(self) -> None:
        """Initialize the EmployeePotential class."""
        self.input_file = '{0}Capacity.xlsx'.format(input_path)
        self.output_file = '{0}CapacityUtilization.xlsx'.format(output_path)
        self.excel_handler = ExcelHandler()

    def process_data(self) -> 'Capacity':
        """Process the data.

        Set column names and forward fill 'Year' values.

        Returns:
            Capacity: An instance of the Capacity class.
        """
        self.excel_handler.df.columns = [
            'Year', 'Quartal', 'Capacity',
            ]
        self.excel_handler.df.with_columns(pl.col('Year').forward_fill())
        return self

    def run_it_all(self):
        """Execute all the steps to process the unemployment data."""
        self.excel_handler.read_data(
            excel_stream=self.input_file,
            sheet_name='Data',
            skip_rows=31,
            has_header=True,
            columns=[0, 1, 2],
            )
        self.process_data()
        self.excel_handler.write_data(output_file=self.output_file)


if __name__ == '__main__':
    Capacity().run_it_all()
