"""Output for Employment potential calculation."""
import polars as pl
from __init__ import input_path, output_path

employee_potential = pl.read_excel(
    '{0}_Sentiment.xlsx'.format(input_path),
    sheet_name='Data',
    engine='calamine',
    read_options={'header_row': 1, 'use_columns': [0, 1, 3]},
    )
employee_potential.columns = ['Year', 'Month', 'Shortage of Employees']
employee_potential = employee_potential.with_columns(
    pl.col('Year').forward_fill(),
    )
employee_potential.write_excel(
    '{0}_EmploymentPotential.xlsx'.format(output_path),
    worksheet='EmploymentPotential',
    )
