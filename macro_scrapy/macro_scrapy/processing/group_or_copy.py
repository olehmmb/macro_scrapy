from datetime import datetime as dt
import polars as pl
import numpy as np
import shutil
import os

current_date = dt.now()
folder_name = current_date.strftime("%Y%m%d")

def groupIntoFolder(typeOfFile):
    source_dir = fr"C:\Users\212627578\PythonProjects\macro_scrapy\data\{folder_name}\input"
    destination_dir = fr"C:\Users\212627578\PythonProjects\macro_scrapy\data\{folder_name}\input\{folder_name}_{typeOfFile}"

    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Group the respective files into the destination
    for filename in os.listdir(source_dir):
        if fr"{typeOfFile}" in filename:
            file_path = os.path.join(source_dir, filename)
            shutil.move(file_path, destination_dir)

def copyToOutput(file):
    source_file = fr"C:\Users\212627578\PythonProjects\macro_scrapy\data\{folder_name}\input\{folder_name}_{file}"
    destination_folder = fr"C:\Users\212627578\PythonProjects\macro_scrapy\data\{folder_name}\output"

    filename = os.path.basename(source_file)
    new_filename = os.path.splitext(filename)[0] + '_tr' + os.path.splitext(filename)[1]
    destination_file = os.path.join(destination_folder, new_filename)

    # Copy the file to the destination folder with the new filename
    shutil.copy(source_file, destination_file)

files_to_group = ["Retail", "ForeignTrade", "IndustrialEvolution", "IndustrialOrders"]
files_to_copy = []

for typeOfFile in files_to_group:
    groupIntoFolder(typeOfFile)

for file in files_to_copy:
    copyToOutput(file)