"""Output for Employment potential calculation."""
import polars as pl
from __init__ import input_path, output_path


class EmployeePotential:
    """A class to handle the processing of employee potential data."""

    def __init__(self, input_file: str, output_file: str) -> None:
        """
        Initialize the EmployeePotential class with input and output paths.

        Parameters:
            input_file: The path to the input folder and prefix.
            output_file:  The path to the output folder and prefix.
        """
        self.input_file_path = '{0}_Sentiment.xlsx'.format(input_file)
        self.output_file_path = ('{0}_EmploymentPotential.xlsx'.format(
            output_file,
            ))

    def read_data(self) -> pl.DataFrame:
        """
        Read the data from an Excel file.

        Returns:
            pl.DataFrame: A Polars DataFrame containing the data from the
            Excel file.
        """
        return pl.read_excel(
            self.input_file_path,
            sheet_name='Data',
            read_options={'skip_rows': 1, 'columns': [0, 1, 3]},
        )

    def process_data(self, raw_data: pl.DataFrame) -> pl.DataFrame:
        """Process the data.

        Set column names and forward fill 'Year' values.

        Parameters:
            raw_data (pl.DataFrame): A Polars DataFrame with the raw data.

        Returns:
            pl.DataFrame: A Polars DataFrame with the processed data.
        """
        raw_data.columns = ['Year', 'Month', 'Shortage of Employees']
        return raw_data.with_columns(pl.col('Year').forward_fill())

    def write_data(self, processed_data: pl.DataFrame) -> None:
        """Write the processed data to an Excel file.

        Parameters:
            processed_data (pl.DataFrame): A Polars DataFrame with
                the processed data to be written to the Excel file.
        """
        processed_data.write_excel(self.output_file_path)


if __name__ == '__main__':
    employee_potential = EmployeePotential(input_path, output_path)
    raw_data = employee_potential.read_data()
    processed_data = employee_potential.process_data(raw_data)
    employee_potential.write_data(processed_data)
