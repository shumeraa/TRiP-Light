        if not (pref_cell.fill.start_color.index in ['00000000', 'FF000000'] or 
                pref_cell.fill.end_color.index in ['00000000', 'FF000000']):
            col_letter = get_column_letter(prefXY[1] + 1)
            print(
                f"WARNING: Black highlighted cell found for leader '{name}' in {os.path.basename(file_path)}.\n"
                f"  - Cell: {col_letter}{currentRow + 2}\n"
                f"  - Value: {prefsDF.iloc[currentRow, prefXY[1]]}"
            )
