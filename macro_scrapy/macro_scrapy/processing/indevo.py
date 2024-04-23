import polars as pl
from __init__ import (
    combine_lists_monthly,
    current_year,
    folder_name,
    list_growth,
    monthly_data,
    parent_folder,
    row_selection,
)

file_name = "IndustrialEvolution"
row = 5
columns = [207, 71, 21]

yearly_indevo_df = pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_{file_name}_Y.xlsx")
quarterly_indevo_df = pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_{file_name}_Q.xlsx")
monthly_indevo_df = pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_{file_name}_M.xlsx")

monthly_indevo_df = row_selection(monthly_indevo_df, row, columns[0])
quarterly_indevo_df = row_selection(quarterly_indevo_df, row, columns[1])
yearly_indevo_df = row_selection(yearly_indevo_df, row, columns[2])

renamed_df_m = monthly_indevo_df.select(pl.col("column_0").cast(pl.Float64).alias("Industrial Production"))
renamed_df_q = quarterly_indevo_df.select(pl.col("column_0").cast(pl.Float64).alias("Industrial Production"))
renamed_df_y = yearly_indevo_df.select(pl.col("column_0").cast(pl.Float64).alias("Industrial Production"))

growth_m = list_growth(renamed_df_m)
growth_q = list_growth(renamed_df_q)
growth_y = list_growth(renamed_df_y)

final_list = combine_lists_monthly(growth_m, growth_q, growth_y)
date_list = monthly_data(current_year - 2018)

final_list = final_list + [0] * (len(date_list) - len(final_list))
final_df = pl.DataFrame({"Time": date_list, "Industrial Production Growth": final_list})
final_df.write_excel(fr"{parent_folder}\data\{folder_name}\output\{folder_name}_IndustrialEvolution.xlsx", worksheet = "IndEvo")
