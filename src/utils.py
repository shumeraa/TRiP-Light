"""Utility functions for converting Excel cell references to DataFrame indices.

This module provides functions to parse Excel-style cell references (e.g., "B2")
and convert them to zero-indexed DataFrame coordinates for pandas operations.
"""

from typing import Any, List, Tuple, Union


def check_if_excel_cell(cell: Any) -> bool:
    """Check if a value is a valid Excel cell reference.

    Args:
        cell: Value to check, expected to be a string like "B2" or "C15".

    Returns:
        True if the value is a valid Excel cell reference (letter followed by digits),
        False otherwise.

    Examples:
        >>> check_if_excel_cell("B2")
        True
        >>> check_if_excel_cell("123")
        False
    """
    if isinstance(cell, str) and cell[0].isalpha() and cell[1:].isdigit():
        return True
    return False


def reformat_cells(
    value: Union[str, int, List[str]],
) -> Union[Tuple[int, int], List[Tuple[int, int]], int, str]:
    """Convert Excel cell references to DataFrame indices.

    Processes single cell references, lists of cell references, or passes through
    non-cell values unchanged. This is the main entry point for cell conversion.

    Args:
        value: Either an Excel cell reference string (e.g., "B2"),
               a list of cell references (e.g., ["C15", "D15"]),
               or a non-cell value like an integer or filename string.

    Returns:
        - For single cells: tuple of (row_index, col_index)
        - For cell lists: list of (row_index, col_index) tuples
        - For other values: the original value unchanged

    Raises:
        ValueError: If a list contains invalid cell references.

    Examples:
        >>> reformat_cells("B2")
        (0, 1)
        >>> reformat_cells(["C15", "D15"])
        [(13, 2), (13, 3)]
        >>> reformat_cells(47)
        47
    """
    if check_if_excel_cell(value):
        return excel_to_df_indices(value)
    elif isinstance(value, list):
        reformatedCellList = []
        for cell in value:
            if check_if_excel_cell(cell):
                reformatedCellList.append(excel_to_df_indices(cell))
            else:
                raise ValueError(
                    f"Expected each value in variable list '{value}' to be a cell, "
                    f"but '{cell}' is not a cell."
                )
        return reformatedCellList
    else:
        # Don't reformat if it is not a cell or list of cells
        return value


def excel_to_df_indices(cell_reference: str) -> Tuple[int, int]:
    """Convert an Excel cell reference to zero-indexed DataFrame coordinates.

    Excel files have one empty row at the top that is automatically removed by pandas,
    so this function adjusts row indices accordingly (subtracts 2 instead of 1).

    Args:
        cell_reference: Excel-style cell reference (e.g., "B2", "C15").
                       Must start with a letter and end with digits.

    Returns:
        Tuple of (row_index, col_index) as zero-indexed coordinates.
        For example, "B2" becomes (0, 1).

    Examples:
        >>> excel_to_df_indices("A1")
        (-1, 0)  # Row -1 due to header adjustment
        >>> excel_to_df_indices("B2")
        (0, 1)
        >>> excel_to_df_indices("C15")
        (13, 2)
    """
    # Extract the column letter and row number from the Excel cell reference
    column_letter = cell_reference[0].upper()
    row_number = int(cell_reference[1:])

    # Convert column letter to zero-based index (e.g., "A" -> 0, "B" -> 1)
    colIndex = ord(column_letter) - ord("A")

    # Convert row number to zero-based index (e.g., 1 -> 0, 2 -> 1)
    # Subtract 2 to account for the empty row at the top being automatically removed
    rowIndex = row_number - 2

    return rowIndex, colIndex
