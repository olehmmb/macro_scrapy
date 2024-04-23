import polars as pl
from __init__ import (
    column_selection,
    combine_lists_monthly,
    folder_name,
    monthly_data,
    parent_folder,
)

file_name = "ForeignTrade"

rows = [150, 54, 18]
import_column = 2
export_column = 3

monthly_foreign_df = (pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_{file_name}_M.xlsx"))[:-3]
quarterly_foreign_df = (pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_{file_name}_Q.xlsx"))[:-3]
yearly_foreign_df = (pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_{file_name}_Y.xlsx"))[:-3]

monthly_import = column_selection(monthly_foreign_df, rows[0], import_column)
quarterly_import = column_selection(quarterly_foreign_df, rows[1], import_column)
yearly_import = column_selection(yearly_foreign_df, rows[2], import_column)

monthly_export = column_selection(monthly_foreign_df, rows[0], export_column)
quarterly_export = column_selection(quarterly_foreign_df, rows[1], export_column)
yearly_export = column_selection(yearly_foreign_df, rows[2], export_column)

renamed_df_m_import = monthly_import.select(pl.col("_duplicated_0").cast(pl.Float64).alias("Import"))
renamed_df_q_import = quarterly_import.select(pl.col("_duplicated_0").cast(pl.Float64).alias("Import"))
renamed_df_y_import = yearly_import.select(pl.col("_duplicated_0").cast(pl.Float64).alias("Import"))

renamed_df_m_export = monthly_export.select(pl.col("_duplicated_1").cast(pl.Float64).alias("Export"))
renamed_df_q_export = quarterly_export.select(pl.col("_duplicated_1").cast(pl.Float64).alias("Export"))
renamed_df_y_export = yearly_export.select(pl.col("_duplicated_1").cast(pl.Float64).alias("Export"))

df_m_import = (renamed_df_m_import["Import"] / renamed_df_m_import["Import"].shift(12))[12:]
df_q_import = (renamed_df_q_import["Import"] / renamed_df_q_import["Import"].shift(4))[4:]
df_y_import = (renamed_df_y_import["Import"] / renamed_df_y_import["Import"].shift(1))[1:]

df_m_export = (renamed_df_m_export["Export"] / renamed_df_m_export["Export"].shift(12))[12:]
df_q_export = (renamed_df_q_export["Export"] / renamed_df_q_export["Export"].shift(4))[4:]
df_y_export = (renamed_df_y_export["Export"] / renamed_df_y_export["Export"].shift(1))[1:]

final_list_import = combine_lists_monthly(df_m_import, df_q_import, df_y_import)
final_list_export = combine_lists_monthly(df_m_export, df_q_export, df_y_export)
date_list = monthly_data(6)

final_list_import = final_list_import + [0] * (len(date_list) - len(final_list_import))
final_list_export = final_list_export + [0] * (len(date_list) - len(final_list_export))

final_df = pl.DataFrame({"Time": date_list, "Import": final_list_import, "Export": final_list_export})
final_df.write_excel(fr"{parent_folder}\data\{folder_name}\output\{folder_name}_ForeignTrade.xlsx", worksheet = "ForeignTrade")
