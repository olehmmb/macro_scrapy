import polars as pl
from __init__ import folder_name, parent_folder

emppot_df = pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_Sentiment.xlsx", sheet_name="Data")

def emppottransformation(df: pl.DataFrame) -> pl.DataFrame:
    intial_df = pl.DataFrame(df)
    trimmed_df = intial_df.select("Bariéry průmysl", "_duplicated_2")
    trimmed_df = trimmed_df.slice(1,len(trimmed_df))

    num_years = len(trimmed_df) // 4
    last_year_rows = len(trimmed_df) % 4

    years = pl.Series([year for year in range(2005, 2005 + num_years) for i in range(4)])
    years.extend(pl.Series([2005 + num_years] * last_year_rows))

    df_final = trimmed_df.with_columns(year=years)
    df_final.columns = ["Month", "Shortage of Employees", "Year"]
    df_final.write_excel(fr"{parent_folder}\data\{folder_name}\output\{folder_name}_EmploymentPotential.xlsx", worksheet = "EmploymentPotential")

emppottransformation(emppot_df)
