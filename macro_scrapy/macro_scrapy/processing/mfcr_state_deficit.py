"""Main module for processing MFCR state deficit data for years 2018--now()."""
import polars as pl
import os
from __init__ import ExcelHandler, input_path, output_path, folder_name
from pathlib import Path


class MFCRStateDeficitData:
    """A class to process MFCR state deficit data exchange rates from a list...

    of .csv files.
    """

    def __init__(self):
        """Initialize MFCRStateDeficitData with necessary attributes."""
        self.data_location = os.listdir(
            '/workspaces/macro_scrapy/data/{0}/input'.format(folder_name),
        )
        self.state_deficit_final = pl.DataFrame()
        self.output_file = '{0}MFCR_State_Deficit.xlsx'.format(output_path)
        self.excel_handler = ExcelHandler()

    def rename_and_drop_columns(self) -> 'MFCRStateDeficitData':
        """Rename columns and drop 'Příjmy' and 'Výdaje'.

        Returns:
            MFCRStateDeficitData: An instance of the MFCRStateDeficitData
            class.
        """
        self.excel_handler.df.columns = [
            'month', 'Příjmy', 'Výdaje', 'saldo', 'datum',
        ]
        self.excel_handler.df = self.excel_handler.df.drop(
            ['Příjmy', 'Výdaje'],
        )
        return self

    def clean_data(self) -> 'MFCRStateDeficitData':
        """Clean up the current dataframe.

        Replace decimal comma with decimal dot.
        Remove invisible UTF characters (non-breaking spaces).
        Change the data type of column 'saldo' to Float64.
        Drop all rows that have a 'NA' in 'saldo' column.

        Returns:
            MFCRStateDeficitData: An instance of the MFCRStateDeficitData
            class.
        """
        self.excel_handler.df = (self.excel_handler.df.with_columns(
            pl.col(
                ['saldo'],
            ).str.replace(
                ',', '.', literal=True,
            ).str.replace(
                '\xa0', '', literal=True,
            ).cast(
                pl.Float64, strict=False,
            )).drop_nulls(
                subset=['saldo'],
            )
        )
        return self

    def get_last_observation_and_stack_it(self) -> 'MFCRStateDeficitData':
        """Get the last observation of the dataframe.

        Get rid of first n-1 rows.
        Convert 'datum' from String to Datetime.
        Add the current dataframe (nrow=1) to
        self.state_deficit_final.

        Returns:
            MFCRStateDeficitData: An instance of the MFCRStateDeficitData
            class.
        """
        self.excel_handler.df = (self.excel_handler.df.slice(
            self.excel_handler.df.height - 1,
        ).with_columns(
            pl.col('datum').str.to_datetime('%d.%m.%Y', strict=False),
            )
        )
        self.state_deficit_final = self.state_deficit_final.vstack(
            self.excel_handler.df, in_place=True,
        )
        return self

    def process_all_csvs(self) -> 'MFCRStateDeficitData':
        """Extract data from all .csv files of type 'MFCR_state_deficit'.

        Then process each dataframe using previous methods.
        """
        files_list = [
            Path(mfcr_file)
            for mfcr_file in self.data_location
            if 'state_deficit' in mfcr_file
        ]
        for curr_file in files_list:
            self.excel_handler.read_data_csv(
                source='{0}{1}'.format(input_path[:-9], curr_file),
                has_header=False,
                encoding='utf8-lossy',
                missing_utf8_is_empty_string=True,
            )
            self.rename_and_drop_columns(
            ).clean_data(
            ).get_last_observation_and_stack_it(
            )

    def clean_up_state_deficit_final(self) -> 'MFCRStateDeficitData':
        """Get the last observation of the dataframe.

        Get the month of the observation.
        Get the correct year of the observation:
        note that for december the data is always
        published in January.
        Rearrange the columns.

        Returns:
            MFCRStateDeficitData: An instance of the MFCRStateDeficitData
            class.
        """
        self.state_deficit_final = (self.state_deficit_final.with_columns(
            pl.when(
                pl.col('month') == 'Prosinec',
            ).then(
                pl.col('datum').dt.year() - 1,
            ).otherwise(
                pl.col('datum').dt.year(),
            ).alias(
                'year',
            )).select(
                ['datum', 'year', 'month', 'saldo'],
            ))
        return self

    def run_it_all(self):
        """Execute all the steps to process the MFCRStateDeficitData data.

        This method performs the following steps:
        Finds all csvs of the 'state_deficit' typ.
        Renames and drops some columns.
        Removes non-breaking spaces from all strings.
        Takes the last row and binds it to self.state_deficit_final.
        Cleans up the self.state_deficit_final and saves the output.
        Returns:
        MFCRStateDeficitData: An instance of the MFCRStateDeficitData
        class.
        """
        self.process_all_csvs()
        self.clean_up_state_deficit_final()
        self.excel_handler.df = self.state_deficit_final
        self.excel_handler.write_data(output_file=self.output_file)


if __name__ == '__main__':
    MFCRStateDeficitData().run_it_all()
