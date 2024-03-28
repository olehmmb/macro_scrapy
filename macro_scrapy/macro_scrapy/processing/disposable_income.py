import os
import shutil
from pathlib import Path

import polars as pl
from __init__ import folder_name, parent_folder, quarterly_data

df = pl.read_csv(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_Households_DisposableIncome.csv")
df = pl.DataFrame(df[["Value"]])
df = df[3:]

chunk_size = 4
num_chunks = len(df) // chunk_size
averages = []

for i in range(num_chunks):
    start = i * chunk_size
    end = (i + 1) * chunk_size
    chunk = df[start:end,0]
    avg = chunk.mean()
    averages.append(avg)

series = df.select("Value").to_series() 
series2 = series.to_list()

print(series2)
print(averages)
