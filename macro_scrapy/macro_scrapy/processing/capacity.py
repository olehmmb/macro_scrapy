import polars as pl
from __init__ import (
    average_every_4,
    current_year,
    folder_name,
    parent_folder,
    quarterly_data,
)

file_name = "Capacity"
capacity_df = (pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_{file_name}.xlsx", sheet_name="Data"))[99:,2]
year_diff = current_year - 2018
time_column = quarterly_data(year_diff)

def capacity(series: pl.Series) -> pl.Series:
    capacities = series.to_list()
    capacities_qy = average_every_4(capacities)
    capacities_qy_final = capacities_qy + [0] * (len(time_column) - len(capacities_qy))
    return capacities_qy_final

capacities_qy_final = capacity(capacity_df)

final_df = pl.DataFrame({"Time": time_column, "Capacity Utilization": capacities_qy_final})
final_df.write_excel(fr"{parent_folder}\data\{folder_name}\output\{folder_name}_Capacity.xlsx", worksheet = "Capacity")
