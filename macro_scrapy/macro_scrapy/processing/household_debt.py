import polars as pl
from __init__ import folder_name, parent_folder, yearly_data


def calculate_v4(df: pl.DataFrame) -> pl.Series:
    pl_series = df.filter(pl.col("LOCATION") == "POL")[["Value"]]
    hu_series = df.filter(pl.col("LOCATION") == "HUN")[["Value"]]
    svk_series = df.filter(pl.col("LOCATION") == "SVK")[["Value"]]
    v4_df = pl.DataFrame({"poland":pl_series, "hungary":hu_series, "slovakia":svk_series})
    return ((v4_df.with_columns(mean=pl.mean_horizontal("poland", "hungary", "slovakia")))["mean"])

def calculate_household_debt(df: pl.DataFrame) -> pl.DataFrame:
    cze_series = df.filter(pl.col("LOCATION") == "CZE")[["Value"]]
    de_series = df.filter(pl.col("LOCATION") == "DEU")[["Value"]]
    years = yearly_data(len(cze_series)-1)
    final_df = pl.DataFrame({"Time":years, "Czechia":cze_series, "Germany":de_series, "V4":calculate_v4(df)})
    final_df.write_excel(fr"{parent_folder}\data\{folder_name}\output\{folder_name}_HouseholdsDebt.xlsx", worksheet = "HouseholdsDebt")

final_df = pl.read_csv(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_Households_Debt.csv")
calculate_household_debt(final_df)
