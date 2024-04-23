import polars as pl
from __init__ import average_every_4, folder_name, parent_folder, quarterly_data


def trimming_df(df: pl.DataFrame) -> list:
    df_trimmed = [float(i) if i is not None and i != "null" else None for i in df[7:,4]]
    df_trimmed = [i if i is not None else 0 for i in df_trimmed]
    num_years = (len(df_trimmed) // 4) + (len(df_trimmed) % 4 > 0)
    time = quarterly_data(num_years)
    return df_trimmed, time

def savings_dataframe(df_trimmed: list, time: list) -> pl.DataFrame:
    final_values = average_every_4(df_trimmed)
    temp_df = {"Time": time,
        "Saving Rate": final_values}
    temp_df["Saving Rate"] += [0] * (len(time) - len(final_values))
    final_df = pl.DataFrame(temp_df)
    final_df.write_excel(fr"{parent_folder}\data\{folder_name}\output\{folder_name}_Savings.xlsx", worksheet = "SavingRate")

savings_df = pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_Savings.xlsx")
df_output, time_output = trimming_df(savings_df)
savings_dataframe(df_output, time_output)
