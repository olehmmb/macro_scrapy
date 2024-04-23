import polars as pl
from __init__ import (
    column_selection,
    combine_lists_monthly,
    current_year,
    folder_name,
    list_growth,
    monthly_data,
    parent_folder,
)

file_name = "ForeignTrade"

rows = [162, 58, 19]
import_column = 8
export_column = 7

monthly_foreign_df = (pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_{file_name}_M.xlsx"))[:-3]
quarterly_foreign_df = (pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_{file_name}_Q.xlsx"))[:-3]
yearly_foreign_df = (pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_{file_name}_Y.xlsx"))[:-3]

monthly_import = column_selection(monthly_foreign_df, rows[0], import_column)
quarterly_import = column_selection(quarterly_foreign_df, rows[1], import_column)
yearly_import = column_selection(yearly_foreign_df, rows[2], import_column)

monthly_export = column_selection(monthly_foreign_df, rows[0], export_column)
quarterly_export = column_selection(quarterly_foreign_df, rows[1], export_column)
yearly_export = column_selection(yearly_foreign_df, rows[2], export_column)

renamed_df_m_import = monthly_import.select(pl.col("_duplicated_6").cast(pl.Float64).alias("Import"))
renamed_df_q_import = quarterly_import.select(pl.col("_duplicated_6").cast(pl.Float64).alias("Import"))
renamed_df_y_import = yearly_import.select(pl.col("_duplicated_6").cast(pl.Float64).alias("Import"))

renamed_df_m_export = monthly_export.select(pl.col("_duplicated_5").cast(pl.Float64).alias("Export"))
renamed_df_q_export = quarterly_export.select(pl.col("_duplicated_5").cast(pl.Float64).alias("Export"))
renamed_df_y_export = yearly_export.select(pl.col("_duplicated_5").cast(pl.Float64).alias("Export"))

growth_m_import = list_growth(renamed_df_m_import)
growth_q_import = list_growth(renamed_df_q_import)
growth_y_import = list_growth(renamed_df_y_import)

growth_m_export = list_growth(renamed_df_m_export)
growth_q_export = list_growth(renamed_df_q_export)
growth_y_export = list_growth(renamed_df_y_export)

final_list_import = combine_lists_monthly(growth_m_import, growth_q_import, growth_y_import)
final_list_export = combine_lists_monthly(growth_m_export, growth_q_export, growth_y_export)
date_list = monthly_data(current_year - 2018)

final_list_import = final_list_import + [0] * (len(date_list) - len(final_list_import))
final_list_export = final_list_export + [0] * (len(date_list) - len(final_list_export))

final_df = pl.DataFrame({"Time": date_list, "Import": final_list_import, "Export": final_list_export})
final_df.write_excel(fr"{parent_folder}\data\{folder_name}\output\{folder_name}_ForeignTrade.xlsx", worksheet = "ForeignTrade")
