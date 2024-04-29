"""Output for MPSV unemployment calculation."""
from datetime import date
from zipfile import ZipFile

import polars as pl
from __init__ import input_path, output_path

series_start = date(1991, 1, 31)

unemployment_mpsv = pl.read_excel(
    ZipFile(
        '{0}_Unemployment.zip'.format(input_path), 'r',
        ).open('2. Nez 2022_2024.xlsx'),
    sheet_name='List1',
    read_options={'skip_rows': 1, 'has_header': False},
    ).head(2).transpose(column_names='column_1')

unemployment_mpsv = unemployment_mpsv.with_columns(
    date=pl.date_range(
        series_start,
        pl.Series([series_start]).dt.offset_by('{0}mo'.format(
            unemployment_mpsv.shape[0] - 1,
            ),
            ), '1mo',
        eager=True,
            ),
)

unemployment_mpsv.write_excel(
    '{0}_UnemployedVacancies.xlsx'.format(output_path),
    worksheet='UnemployedVacancies',
    )
