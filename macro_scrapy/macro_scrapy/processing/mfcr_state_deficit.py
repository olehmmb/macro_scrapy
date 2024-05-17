"""Main module for processing MFCR state deficit data for years 2018--now()."""
import polars as pl
from __init__ import ExcelHandler, input_path, output_path


class MFCRStateDeficitData:
    """A class to process MFCR state deficit data exchange rates from a csv."""

    def __init__(self):
        """Initialize MFCRStateDeficitData with necessary attributes."""
        self.input_file = '{0}MFCR_state_deficit.csv'.format(input_path)
        self.output_file = '{0}MFCR_State_Deficit.xlsx'.format(output_path)
        self.excel_handler = ExcelHandler()

    def rename_and_drop_columns(self) -> 'MFCRStateDeficitData':
        """Drop 'Příjmy' and 'Výdaje' and rename columns.

        Returns:
            MFCRStateDeficitData: An instance of the MFCRStateDeficitData
            class.
        """
        self.excel_handler.df = self.excel_handler.df.drop(
            ['Příjmy', 'Výdaje'],
        ).rename(
            {'2024': 'year',
             'Tisková  zpráva': 'date_published',
             'Měsíc': 'month',
             'Saldo': 'saldo',
             },
        )

        return self

    def clean_data(self) -> 'MFCRStateDeficitData':
        """Clean up the current dataframe.

        Remove invisible UTF characters (non-breaking spaces).
        Change the data type of column 'saldo' to Float64.
        Drop all rows that have a 'NA' in 'saldo' column.
        Convert 'date_published' to Datetime.

        Returns:
            MFCRStateDeficitData: An instance of the MFCRStateDeficitData
            class.
        """
        self.excel_handler.df = (self.excel_handler.df.with_columns(
            pl.col(
                ['saldo'],
            ).str.replace(
                '\xa0', '', literal=True,
            ).cast(
                pl.Float64, strict=False,
            )).drop_nulls(
                subset=['saldo'],
            ).with_columns(
                pl.col('date_published').str.to_datetime(
                '%d.%m.%Y', strict=False,
                ),
            )
        )
        return self

    def leave_last_rows(self) -> 'MFCRStateDeficitData':
        """Get the last observation of the dataframe.

        Aggregate by year and get the last observation.
        Rearrange columns.

        Returns:
            MFCRStateDeficitData: An instance of the MFCRStateDeficitData
            class.
        """
        self.excel_handler.df = (self.excel_handler.df.group_by(
            'year',
        ).agg(
            pl.all().last(),
        ).select(
            'date_published', 'year', 'month', 'saldo',
        ).sort(
            'date_published',
        )
        )
        return self

    def run_it_all(self):
        """Execute all the steps to process the MFCRStateDeficitData data.

        This method performs the following steps:
        Renames all and drops some columns.
        Removes non-breaking spaces from all strings and changes datatypes
        of 'saldo' and 'date_published' columns.
        Leaves the last row (available observation) for each year only.
        Rearranges columns.

        Returns:
        MFCRStateDeficitData: An instance of the MFCRStateDeficitData
        class.
        """
        self.excel_handler.read_data_csv(
            source=self.input_file,
            has_header=True,
            encoding='utf8-lossy',
            missing_utf8_is_empty_string=True,
        )
        self.rename_and_drop_columns(
        ).clean_data(
        ).leave_last_rows()
        self.excel_handler.write_data(output_file=self.output_file)


if __name__ == '__main__':
    MFCRStateDeficitData().run_it_all()
