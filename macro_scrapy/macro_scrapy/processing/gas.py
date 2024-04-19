import contextlib
import os
import zipfile

import polars as pl
from __init__ import current_year, folder_name, monthly_data_no_QY, parent_folder
from xls2xlsx import XLS2XLSX

zip_file = "Gas.zip"
folder_path = fr"{parent_folder}\data\{folder_name}"
zip_file_path = fr"{parent_folder}\data\{folder_name}\input\{folder_name}_{zip_file}"

file_to_extract = "Rocni_zprava_o_trhu_plyn_2024_V0.xls"
destination_folder = fr"{parent_folder}\data\{folder_name}\input"

with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
    zip_ref.extract(file_to_extract, destination_folder)

file_extracted = XLS2XLSX(fr"{parent_folder}\data\{folder_name}\input\Rocni_zprava_o_trhu_plyn_2024_V0.xls")
file_extracted.to_xlsx(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_Gas.xlsx")

os.remove(fr"{parent_folder}\data\{folder_name}\input\Rocni_zprava_o_trhu_plyn_2024_V0.xls")

gas_df = pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_Gas.xlsx", sheet_name = "VDT")
averages = list(filter(lambda x: x is not None, (gas_df.select("_duplicated_19").to_series()).to_list()))
averages = averages[1:]

if (current_year % 4 == 0):
    indices = [32, 61, 92, 122, 153, 183, 214, 244, 265, 294, 325, 355]
else:
    indices = [32, 61, 93, 123, 154, 184, 215, 245, 266, 295, 326, 356]

ends_of_month =  []

for index in indices:
    try:
        value = gas_df[index, 2]
        ends_of_month.append(value)
    except IndexError:  # noqa: PERF203
        continue

historical_averages = [19.28, 18.19, 18.32, 21.37, 25.82, 29.74, 36.41, 44.74, 63.36, 87.44, 85.26, 114, 83, 81, 125, 100, 89, 101, 174, 243, 192, 66, 88, 118, 64, 55, 47, 45, 34, 34, 31, 37, 38, 44, 45, 38]
historical_ends_of_month = [19.27, 16.68, 19.5, 24.36, 25.81, 35.7, 40.18, 49.9, 91.51, 66.06, 96.48, 76.99, 87, 106, 123, 95, 91, 148, 192, 257, 168, 50, 142, 70, 60, 50, 48, 40, 28, 37, 28, 37, 39, 43, 45, 31]

def average_every_12(lst):
    for i in range(0, len(lst), 13):
        group = lst[i:i+12]
        group_average = sum(group)/len(group)
        lst.insert(i+12, group_average)

average_every_12(historical_averages)
average_every_12(historical_ends_of_month)

historical_averages.extend(averages)
historical_ends_of_month.extend(ends_of_month)

time_column = monthly_data_no_QY(3)
hist_avg = historical_averages + [0] * (len(time_column) - len(historical_averages))
hist_end = historical_ends_of_month + [0] * (len(time_column) - len(historical_ends_of_month))

for i in range(len(hist_avg)):
    if hist_avg[i] is not None:
        with contextlib.suppress(ValueError):
            hist_avg[i] = float(hist_avg[i])

for i in range(len(hist_end)):
    if hist_end[i] is not None:
        with contextlib.suppress(ValueError):
            hist_end[i] = float(hist_end[i])

final_df = pl.DataFrame({"Time": time_column, "Average": hist_avg, "End of month": hist_end})
final_df.write_excel(fr"{parent_folder}\data\{folder_name}\output\{folder_name}_Gas.xlsx", worksheet = "Gas")
