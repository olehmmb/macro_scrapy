import polars as pl
from __init__ import average_every_4, folder_name, parent_folder

row =5
file_name = "_IndustrialEvolution_"
columns = [21, 71, 207]
names = ["Y", "Q", "M"]


yearly_indevo_df = pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_IndustrialEvolution_Y.xlsx")
quarterly_indevo_df = pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_IndustrialEvolution_Q.xlsx")
monthly_indevo_df = pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_IndustrialEvolution_M.xlsx")

yearly_indevo_df = yearly_indevo_df[5,21:]
yearly_indevo_df = yearly_indevo_df.transpose(include_header=False)
formatted_df_y = yearly_indevo_df.select(pl.col("column_0").cast(pl.Float64).alias("Industrial Production"))

quarterly_indevo_df = quarterly_indevo_df[5,71:]
quarterly_indevo_df = quarterly_indevo_df.transpose(include_header=False)
formatted_df_q = quarterly_indevo_df.select(pl.col("column_0").cast(pl.Float64).alias("Industrial Production"))

monthly_indevo_df = monthly_indevo_df[5,207:]
monthly_indevo_df = monthly_indevo_df.transpose(include_header=False)
formatted_df_m = monthly_indevo_df.select(pl.col("column_0").cast(pl.Float64).alias("Industrial Production"))

growth_yoy = []
growth_q = []
growth_m = []

for i in formatted_df_y:
    growth = i-100
    growth_yoy.append(growth)

for i in formatted_df_q:
    growth = i-100
    growth_q.append(growth)

for i in formatted_df_m:
    growth = i-100
    growth_m.append(growth)

