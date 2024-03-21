from datetime import datetime as dt

import polars as pl

current_date = dt.now(tz=dt.timezone.cet)
folder_name = current_date.strftime("%Y%m%d")

emppot_df = pl.read_excel(fr"C:\Users\212627578\PythonProjects\macro_scrapy\data\{folder_name}\input\{folder_name}_Sentiment.xlsx", sheet_name="Data")

def emppottransformation(df: pl.df) -> pl.df:
    intial_df = pl.DataFrame(df)
    trimmed_df = intial_df.select("Bariéry průmysl", "_duplicated_2")
    trimmed_df = trimmed_df.slice(1,len(trimmed_df))

    num_years = len(trimmed_df) // 4
    last_year_rows = len(trimmed_df) % 4

    years = pl.Series([year for year in range(2005, 2005 + num_years)
                        for i in range(4)])
    years.extend(pl.Series([2005 + num_years] * last_year_rows))

    df_final = trimmed_df.with_columns(year=years)
    df_final.columns = ["Month", "Shortage of Employees", "Year"]
    df_final.write_excel(fr"C:\Users\212627578\PythonProjects\macro_scrapy\data\{folder_name}\output\{folder_name}_EmploymentPotential.xlsx", worksheet = "EmploymentPotential")

emppottransformation(emppot_df)
