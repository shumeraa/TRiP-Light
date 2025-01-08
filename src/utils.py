import pandas as pd


def check_if_excel_cell(cell):
    if isinstance(cell, str) and cell[0].isalpha() and cell[1:].isdigit():
        return True
    return False


def reformat_cells_manager(value):
    # if value is excel cell
    if check_if_excel_cell(value):
        return excel_to_df_indices(value)
    # if it is a list of excel cells
    elif isinstance(value, list):
        reformatedCellList = []
        for cell in value:
            if check_if_excel_cell(cell):
                reformatedCellList.append(excel_to_df_indices(cell))
            else:
                raise ValueError(
                    f"Expected each value in variable list '{value}' to be a cell, but '{cell}' is not a cell."
                )
        return reformatedCellList
    else:
        # Don't reformat if it is not a cell or list of cells
        return value


def excel_to_df_indices(cell_reference):
    # Extract the column letter and row number from the Excel cell reference
    column_letter = cell_reference[0].upper()
    row_number = int(cell_reference[1:])

    # Convert column letter to zero-based index (e.g., "A" -> 0, "B" -> 1)
    colIndex = ord(column_letter) - ord("A")

    # Convert row number to zero-based index (e.g., 1 -> 0, 2 -> 1)
    # remove 2 to account for the empty row at the top being automatically removed
    rowIndex = row_number - 2

    return rowIndex, colIndex
