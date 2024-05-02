import eurostat
import polars as pl
from __init__ import folder_name, parent_folder

data = pl.DataFrame(eurostat.get_data_df("une_rt_m"))
data = data.rename({"geo\\TIME_PERIOD" : "geo"})
data = data.filter(
    pl.col("geo").is_in(["CZ", "EA20", "SK", "PL", "HU"]),
    pl.col("age") == "TOTAL",
    pl.col("unit") == "PC_ACT",
    pl.col("s_adj") == "SA",
    pl.col("sex") == "T")
locations = data["geo"]

final_data = data[:,426:]
final_data = final_data.transpose(include_header=True)
final_data = final_data.rename({"column": "Time",
                  "column_0": locations[0],
                  "column_1": locations[1],
                  "column_2": locations[2],
                  "column_3": locations[3],
                  "column_4": locations[4]})
final_data = final_data.drop_nulls()
final_data = final_data.with_columns(
    V4=((pl.col("HU") + pl.col("SK") + pl.col("PL")) / 3))

final_data = final_data.drop(["HU", "PL", "SK"])
final_data.write_excel(fr"{parent_folder}/data/{folder_name}/output/{folder_name}_UnemploymentEurostat.xlsx", worksheet = "Unemployment")
