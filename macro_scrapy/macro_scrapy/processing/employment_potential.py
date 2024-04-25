import polars as pl
from __init__ import folder_name, parent_folder

employee_potential = pl.read_excel(fr"{parent_folder}/data/{folder_name}/input/{folder_name}_Sentiment.xlsx", sheet_name="Data",engine = "calamine", read_options = {"header_row": 1,"use_columns":[0,1,3]})
employee_potential.columns = ["Year", "Month", "Shortage of Employees"]
employee_potential = employee_potential.with_columns(pl.col("Year").forward_fill())  
employee_potential.write_excel(fr"{parent_folder}/data/{folder_name}/output/{folder_name}_EmploymentPotential.xlsx", worksheet = "EmploymentPotential")


