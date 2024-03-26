import os
import shutil
from pathlib import Path

from __init__ import folder_name, parent_folder


def groupintofolder(typeoffile: str) -> None:
    source_dir = fr"{parent_folder}\data\{folder_name}\input"
    destination_dir = Path(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_{typeoffile}")

    # Create the destination directory if it doesn't exist
    if not Path.exists(destination_dir):
        Path.mkdir(destination_dir)

    # Group the respective files into the destination
    for filename in os.listdir(source_dir):
        if fr"{typeoffile}" in filename:
            file_path = Path(source_dir) / filename
            shutil.move(file_path, destination_dir)

def copytooutput(file: str) -> None:
    source_file = fr"{parent_folder}\data\{folder_name}\input\{folder_name}_{file}"
    destination_folder = fr"{parent_folder}\data\{folder_name}\output"

    filename = Path.name(source_file)
    new_filename = filename
    destination_file = Path(destination_folder) / new_filename

    # Copy the file to the destination folder with the new filename
    shutil.copy(source_file, destination_file)

files_to_group = ["Retail", "ForeignTrade", "IndustrialEvolution", "IndustrialOrders"]
files_to_copy = []

for typeoffile in files_to_group:
    groupintofolder(typeoffile)

for file in files_to_copy:
    copytooutput(file)
