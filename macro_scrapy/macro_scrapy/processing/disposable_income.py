"""Output for Household Disposable Income calculation."""
from __init__ import ExcelHandler, input_path, output_path


class DisposableIncome:
    """A class handling the processing of Households Disposable Income data."""

    def __init__(self, freq) -> None:
        """Initialize the Disposable Income class.

        Args:
            freq: Any number of lists of strings.
        """
        self.freq = freq
        self.input_file = '{0}Households_DisposableIncome_{1}.csv'.format(
            input_path, self.freq,
            )
        self.output_file = '{0}Households_DisposableIncome_{1}.xlsx'.format(
            output_path, self.freq,
            )
        self.excel_handler = ExcelHandler()

    def process_data(self) -> 'DisposableIncome':
        """Process the data.

        Select distinct columns from the initial df.

        Returns:
            IndEvo: An instance of the IndEvo class.
        """
        df = self.excel_handler.df
        df = df.select(['LOCATION', 'Time', 'Value'])
        self.excel_handler.df = df
        return self

    def run_it_all(self):
        """Execute all the steps to process the retail data."""
        self.excel_handler.read_data_csv(
            source=self.input_file,
            has_header=True,
            )
        self.process_data()
        self.excel_handler.write_data(output_file=self.output_file)


if __name__ == '__main__':
    frequencies = [
        ('Q'),
        ('Y'),
        ]

    for freq in frequencies:
        DisposableIncome(freq).run_it_all()
