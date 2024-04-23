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

file_name = "Retail"
row_with_cars = 5
row = 13
columns = [219, 75, 21]

yearly_retail_df = pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_{file_name}_Y.xlsx")
quarterly_retail_df = pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_{file_name}_Q.xlsx")
monthly_retail_df = pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_{file_name}_M.xlsx")

monthly_retail_cars = row_selection(monthly_retail_df, row_with_cars, columns[0])
quarterly_retail_cars = row_selection(quarterly_retail_df, row_with_cars, columns[1])
yearly_retail_cars = row_selection(yearly_retail_df, row_with_cars, columns[2])

monthly_retail = row_selection(monthly_retail_df, row, columns[0])
quarterly_retail = row_selection(quarterly_retail_df, row, columns[1])
yearly_retail = row_selection(yearly_retail_df, row, columns[2])

renamed_df_m_cars = monthly_retail_cars.select(pl.col("column_0").cast(pl.Float64).alias("With Cars"))
renamed_df_q_cars = quarterly_retail_cars.select(pl.col("column_0").cast(pl.Float64).alias("With Cars"))
renamed_df_y_cars = yearly_retail_cars.select(pl.col("column_0").cast(pl.Float64).alias("With Cars"))

renamed_df_m = monthly_retail.select(pl.col("column_0").cast(pl.Float64).alias("Without Cars"))
renamed_df_q = quarterly_retail.select(pl.col("column_0").cast(pl.Float64).alias("Without Cars"))
renamed_df_y = yearly_retail.select(pl.col("column_0").cast(pl.Float64).alias("Without Cars"))

growth_m_cars = list_growth(renamed_df_m_cars)
growth_q_cars = list_growth(renamed_df_q_cars)
growth_y_cars = list_growth(renamed_df_y_cars)

growth_m = list_growth(renamed_df_m)
growth_q = list_growth(renamed_df_q)
growth_y = list_growth(renamed_df_y)

final_list_cars = combine_lists_monthly(growth_m_cars, growth_q_cars, growth_y_cars)
final_list = combine_lists_monthly(growth_m, growth_q, growth_y)
date_list = monthly_data(current_year - 2018)

final_list_cars = final_list_cars + [0] * (len(date_list) - len(final_list))
final_list = final_list + [0] * (len(date_list) - len(final_list))

final_df = pl.DataFrame({"Time": date_list, "With Cars": final_list_cars, "Without Cars": final_list})
final_df.write_excel(fr"{parent_folder}\data\{folder_name}\output\{folder_name}_Retail.xlsx", worksheet = "Retail")
