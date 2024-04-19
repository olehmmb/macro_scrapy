
import polars as pl
from __init__ import folder_name, parent_folder, quarterly_data

df_q = pl.read_csv(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_Households_DisposableIncome_Q.csv")
df_q = pl.DataFrame(df_q[["Value"]])
df_q = df_q[3:]

df_y = pl.read_csv(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_Households_DisposableIncome_Y.csv")
df_y = pl.DataFrame(df_y[["Value"]])

chunk_size = 4
num_chunks = len(df_q) // chunk_size
averages = (df_y.select("Value").to_series()).to_list()
final_series = []

def merge_into_series() -> list:
    index_averages = 0
    series = (df_q.select("Value").to_series()).to_list()
    for i in range(0, len(series), 4):
        final_series.extend(series[i:i+4])
        if index_averages < len(averages):
            final_series.append(averages[index_averages])
            index_averages += 1

def create_disposable_income_df() -> pl.DataFrame:
    quarters = quarterly_data(len(averages)+1)
    difference = len(quarters) - len(final_series)
    quarters = quarters[:-difference]
    df_final = pl.DataFrame({"Time":quarters, "Disposable Income":final_series})
    df_final.write_excel(fr"{parent_folder}\data\{folder_name}\output\{folder_name}_DisposableIncome.xlsx", worksheet = "DisposableIncome")

merge_into_series()
create_disposable_income_df()
