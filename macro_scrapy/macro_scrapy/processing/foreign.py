"""Output for Foreign Trade calculation."""
from __init__ import ExcelHandler, input_path, output_path


class Foreign:
    """A class to handle the processing of Foreign Trade data."""

    def __init__(self, freq) -> None:
        """Initialize the Foreign class.

        Args:
            freq: Any number of lists of strings.
        """
        self.freq = freq
        self.input_file = '{0}ForeignTrade_{1}.xlsx'.format(
            input_path, self.freq,
            )
        self.output_file = '{0}ForeignTrade_{1}.xlsx'.format(
            output_path, self.freq,
            )
        self.excel_handler = ExcelHandler()

    def process_data(self) -> 'Foreign':
        """Process the data.

        Slice the data, transpose the sliced dataframe and choose column names.

        Returns:
            Foreign: An instance of the Foreign class.
        """
        self.excel_handler.df = self.excel_handler.df[2:]
        self.excel_handler.df.columns = [
            'Time',
            'Turnover (abs)',
            'Export (abs)',
            'Import (abs)',
            'Balance',
            'Turnover',
            'Export',
            'Import',
            ]
        return self

    def run_it_all(self):
        """Execute all the steps to process the industrial evolution data."""
        self.excel_handler.read_data(
            excel_stream=self.input_file,
            sheet_name='DATA',
            skip_rows=7,
            has_header=False,
            columns=[1, 2, 3, 4, 5, 6, 7, 8],
            )
        self.process_data()
        self.excel_handler.write_data(output_file=self.output_file)


if __name__ == '__main__':
    frequency = [
        ('M'),
        ('Q'),
        ('Y'),
        ]

    for freq in frequency:
        Foreign(freq).run_it_all()
