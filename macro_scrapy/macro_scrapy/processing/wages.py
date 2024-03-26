import polars as pl
from __init__ import folder_name, parent_folder

wage_df = pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_GrossWage.xlsx", sheet_name="Data")

def wages_transformation(df: pl.DataFrame) -> pl.DataFrame:
    initial_df = pl.DataFrame(df)
    df_trimmed = initial_df.slice(0, -3)
    df_trimmed = df_trimmed.transpose()

    df_trimmed = df_trimmed.select(("Q"+(pl.col("column_0").str.extract(r"^(.).*"))).alias("Quartal"), (pl.col("column_1")).alias("Average Wage"))
    df_final = df_trimmed[1:,:]

    num_years = len(df_final) // 4
    years = pl.Series([year for year in range(2001, 2001 + num_years) for i in range(4)])
    df_final = df_final.with_columns(Year=years)

    df_final.write_excel(fr"{parent_folder}\data\{folder_name}\output\{folder_name}_AverageWage.xlsx", worksheet = "AverageWage")

wages_transformation(wage_df)
