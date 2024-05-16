"""Main module for processing 2W CNB repo data."""
import polars as pl
from __init__ import ExcelHandler, input_path, output_path


class RepoData:
    """A class to process 2W CNB repo rates from an Excel file."""

    def __init__(self):
        """Initialize RepoData with necessary attributes."""
        self.input_file = '{0}REPO.xlsx'.format(input_path)
        self.output_file = '{0}Repo.xlsx'.format(output_path)
        self.excel_handler = ExcelHandler()

    def process_data(self) -> 'RepoData':
        """
        Process data by removing redundant rows and columns.

        Then rename columns and sort the dataframe by 'date' column.

        Returns:
            RepoData: An instance of the RepoData class.
        """
        self.excel_handler.df = (self.excel_handler.df.slice(
            3, len(self.excel_handler.df),
        ).select(
            self.excel_handler.df.columns[:2],
        ).slice(1, len(self.excel_handler.df))
        )
        self.excel_handler.df.columns = ['date', '2W_repo_rate']
        self.excel_handler.df = self.excel_handler.df.sort(
            'date', descending=False,
        )

        return self

    def recast_columns(self) -> 'RepoData':
        """
        Recast columns to the correct data type.

        Returns:
            RepoData: An instance of the RepoData class.
        """
        self.excel_handler.df = self.excel_handler.df.with_columns(
            pl.col('date').cast(pl.Date),
            pl.col('2W_repo_rate').cast(pl.Float32),
        )
        return self

    def create_year_column(self) -> 'RepoData':
        """
        Retrieve the corresponding year for each row.

        Returns:
            RepoData: An instance of the RepoData class.
        """
        self.excel_handler.df = self.excel_handler.df.with_columns(
            pl.col('date').dt.year().alias('year'),
        )
        return self

    def get_end_of_year_values(self) -> 'RepoData':
        """
        Leave only the end-of-year values and rearrange the columns.

        Returns:
            RepoData: An instance of the RepoData class.
        """
        self.excel_handler.df = (
            self.excel_handler.df.group_by(
                'year',
            ).agg(
                pl.col('2W_repo_rate').last().round(1).alias(
                    '2W_repo_rate_eop',
                ),
                pl.col('date').last().alias('date'),
            ).sort(
                pl.col('year'),
            ).select('date', 'year', '2W_repo_rate_eop')
        )
        return self

    def run_it_all(self):
        """
        Execute all the steps to process the REPO data.

        This method performs the following steps:
        Processes the data by removing redundant rows and columns.
        Recasts each column to the correct data type.
        Creates a 'year' column.
        Retrieves end-of-year values only and rearranges columns.
        Writes the DataFrame to an Excel file.
        """
        self.excel_handler.read_data(
            excel_stream=self.input_file,
            has_header=False,
        )
        (self.process_data(
        ).recast_columns(
        ).create_year_column(
        ).get_end_of_year_values()
        )
        self.excel_handler.write_data(output_file=self.output_file)


if __name__ == '__main__':
    RepoData().run_it_all()
