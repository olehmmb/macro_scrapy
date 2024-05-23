"""Output for Employment potential calculation."""
import polars as pl
from __init__ import ExcelHandler, input_path, output_path


class EmployeePotential:
    """A class to handle the processing of employee potential data."""

    def __init__(self) -> None:
        """Initialize the EmployeePotential class."""
        self.input_file = '{0}Sentiment.xlsx'.format(input_path)
        self.output_file = '{0}EmploymentPotential.xlsx'.format(output_path)
        self.excel_handler = ExcelHandler()

    def process_data(self) -> 'EmployeePotential':
        """Process the data.

        Set column names and forward fill 'Year' values.

        Returns:
            EmployeePotential: An instance of the EmployeePotential class.
        """
        self.excel_handler.df.columns = [
            'Year',
            'Month',
            'No limitations',
            'Insufficient demand',
            'Shortage of Employees',
            'Material / Equipment shortage',
            'Financial Constraints',
            'Other limitations',
            ]
        self.excel_handler.df.with_columns(pl.col('Year').forward_fill())
        return self

    def run_it_all(self):
        """Execute all the steps to process the unemployment data."""
        self.excel_handler.read_data(
            excel_stream=self.input_file,
            sheet_name='Data',
            skip_rows=1,
            has_header=True,
            columns=[0, 1, 2, 3, 4, 5, 6, 7],
            )
        self.process_data()
        self.excel_handler.write_data(output_file=self.output_file)


if __name__ == '__main__':
    EmployeePotential().run_it_all()
