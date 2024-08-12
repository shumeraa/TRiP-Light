import os
import pandas as pd
from tripLeaderManager import TripLeaderManager


def get_user_input(header_name):
    return input(f"Please enter the excel cell for the '{header_name}' header: ")


def excel_to_df_indices(cell_reference):
    # Extract the column letter and row number from the Excel cell reference
    column_letter = cell_reference[0].upper()
    row_number = int(cell_reference[1:])

    # Convert column letter to zero-based index (e.g., "A" -> 0, "B" -> 1)
    colIndex = ord(column_letter) - ord("A")

    # Convert row number to zero-based index (e.g., 1 -> 0, 2 -> 1)
    rowIndex = row_number - 1

    return rowIndex, colIndex


def excel_to_df_cell(dates_cell, trip_cell, preferences_cell):
    dates_index = excel_to_df_indices(dates_cell)
    trip_index = excel_to_df_indices(trip_cell)
    preferences_index = excel_to_df_indices(preferences_cell)
    name_index = excel_to_df_indices(name_cell)

    return dates_index, trip_index, preferences_index, name_index

def get_sheet_names(sheet_name):
    return input(f"Please enter the index of the sheet for the '{sheet_name}' sheet (1st sheet is 1): ") - 1


def process_excel_files(dateXY, tripXY, prefXY, nameXY, folder_path="Data"):
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return

    files = [
        f
        for f in os.listdir(folder_path)
        if f.endswith(".xlsx") and not f.startswith("~")
    ]

    if not files:
        print("No valid Excel files found in the folder.")
        return

    trip_leader_manager = TripLeaderManager()
    
    for index, file_name in enumerate(files):
        file_path = os.path.join(folder_path, file_name)

        # Checking if the file is empty
        try:
            df = pd.read_excel(file_path)
            if df.empty:
                print(f"File {file_name} is empty, skipping.")
                continue
        except Exception as e:
            print(f"Could not read {file_name}: {e}")
            continue

        if index == 0:
            
        else:
            print("Not First")
