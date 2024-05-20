"""Main module for processing MFCR Makroekonomicka predikce data."""
import polars as pl
from __init__ import ExcelHandler, input_path, output_path


class MFCRTablesData:
    """
    A class to process MFCR Makroekonomicka predikce data from am...

    .xlsx file.
    """

    def __init__(self):
        """Initialize MFCRTablesData with necessary attributes."""
        self.input_file = '{0}MFCR_Makroekonomicka_predikce_tabulky.xlsx'.format(input_path)
        self.output_file = '{0}mfcr_makroekonomicka_predikce.xlsx'.format(output_path)
        self.forecast_df = pl.DataFrame()
        self.excel_handler = ExcelHandler()

    def get_forecast_column(self) -> 'MFCRTablesData':
        """
        Get forecast column.

        Returns:
            MFCRTablesData: An instance of the MFCRTablesData class.
        """
        self.forecast_df = self.excel_handler.df.slice(
            0, 1,
        ).select(
            [col for col in self.excel_handler.df.columns if col.isdigit()],
        ).transpose(
        ).rename(
            {'column_0': 'forecast?'},
        )

        return self

    def get_the_actual_table(self) -> 'MFCRTablesData':
        """
        Get the actual table.

        Leave only the columns that have rownames or
        actual data in them (2018...2024).
        Create the rownames.
        Get the data for government debt only.

        Returns:
            MFCRTablesData: An instance of the MFCRTablesData class.
        """
        cols_to_select = [
            column
            for column in self.excel_handler.df.columns
            if (
                column.isdigit() or column in
                {'_duplicated_0', '_duplicated_1'}
            )
        ]

        self.excel_handler.df = (
            self.excel_handler.df.select(
                cols_to_select,
            ).rename(
                {'_duplicated_0': 'rownames',
                 '_duplicated_1': 'definition',
                 },
            ).with_columns(
                pl.col('rownames').forward_fill(),
            ).filter((pl.col('rownames') == 'General government debt'))
        )
        return self

    def clean_table(self) -> 'MFCRTablesData':
        """
        Clean the table.

        Rearrange the columns.
        Transpose the dataframe.
        Use the first row of the transposed dataframe as column names.
        Add forecast column to the dataframe.

        Returns:
            MFCRTablesData: An instance of the MFCRTablesData class.
        """
        self.excel_handler.df = self.excel_handler.df.with_columns(
            pl.concat_str(
                [
                    pl.col('rownames'),
                    pl.col('definition'),
                ],
                separator=', ',
            ).alias('row_names'),
        ).drop('rownames', 'definition')

        self.excel_handler.df = self.excel_handler.df.select(
            'row_names', *[
                col
                for col in self.excel_handler.df.columns
                if col != 'row_names'
            ],
        )

        self.excel_handler.df = self.excel_handler.df.transpose(
            include_header=True,
        )
        new_cols_dict = self.excel_handler.df.head(1).to_dicts().pop()
        self.excel_handler.df = (
            self.excel_handler.df.rename(
                new_cols_dict,
            )
        ).slice(
            1,
        ).with_columns(
            pl.all().cast(pl.Float64),
        ).rename(
            {'row_names': 'year'},
        ).hstack(
            self.forecast_df,
        ).fill_null('No')
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
        self.excel_handler.read_data(
            excel_stream=self.input_file,
            has_header=True,
            sheet_name='T 1.3.1',
            skip_rows=6,
        )
        self.get_forecast_column(
        ).get_the_actual_table(
        ).clean_table()
        self.excel_handler.write_data(output_file=self.output_file)


if __name__ == '__main__':
    MFCRTablesData().run_it_all()
