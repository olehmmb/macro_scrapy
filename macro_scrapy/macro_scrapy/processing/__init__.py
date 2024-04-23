"""Processing management package.

This package provides resources for processing.
It introduces variables that are subsequently used for obtaining / storing raw and processed data.
"""
from datetime import datetime as dt
from datetime import timezone

import polars as pl
from xls2xlsx import XLS2XLSX

parent_folder = r"C:\Users\212627578\PythonProjects\macro_scrapy"
current_date = dt.now(tz=timezone.utc)
current_year = current_date.year
folder_name = current_date.strftime("%Y%m%d")

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
date_list =  []

def monthly_data(years: int) -> list:
    for i in range(years, -1, -1):
        specific_year = str(current_year - i)
        for j in range(0, len(months), 3):
            date_list.extend(months[j:j+3])
            if j == 0:
                date_list.append("Q1")
            elif j == 3:
                date_list.append("Q2")
            elif j == 6:
                date_list.append("Q3")
            elif j == 9:
                date_list.append("Q4")
        date_list.append(specific_year)
    return date_list

def quarterly_data(years: int) -> list:
    for i in range(years, -1, -1):
        for j in range(0, len(months), 3):
            if j == 0:
                date_list.append("Q1")
            elif j == 3:
                date_list.append("Q2")
            elif j == 6:
                date_list.append("Q3")
            elif j == 9:
                date_list.append("Q4")
        specific_year = str(current_year - i)
        date_list.append(specific_year)
    return date_list

def yearly_data(years: int) -> list:
    for i in range(years, -1, -1):
        specific_year = str(current_year - i)
        date_list.append(specific_year)
    return date_list

def monthly_data_no_qy(years: int) -> list:
    for i in range(years, -1, -1):
        specific_year = str(current_year - i)
        for j in range(0, len(months), 3):
            date_list.extend(months[j:j+3])
        date_list.append(specific_year)
    return date_list

def convert_xls(file_to_convert):
    convertable = XLS2XLSX(file_to_convert)
    converted_file = convertable.to_xlsx()
    return converted_file

def average_every_4(lst) -> list:
    new_list = []
    for i in range(0, len(lst), 4):
        group = lst[i:i+4]
        group_average = sum(group) / len(group)
        new_list.extend(group)
        new_list.append(group_average)
    return new_list

def combine_lists_monthly(M, Q, Y):
    final_list = []
    index_q = 0
    index_y = 0
    for i, item in enumerate(M):
        final_list.append(item)
        if (i + 1) % 3 == 0 and index_q < len(Q):
            final_list.append(Q[index_q])
            index_q += 1
        if (i + 1) % 12 == 0 and index_y < len(Y):
            final_list.append(Y[index_y])
            index_y += 1
    return final_list

def row_selection(df, row, column):
    df = df[row, column:]
    df = df.transpose(include_header=False)
    return df

def column_selection(df, row, column):
    df = df[row:, column]
    return pl.DataFrame(df)

def list_growth(sequence):
    growth_list = []
    for i in sequence:
        growth = i-100
        growth_list.extend(growth)
    return growth_list
