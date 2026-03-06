import openpyxl
import os

file_path = r'source/Lotto023.xlsx'

if os.path.exists(file_path):
    try:
        wb = openpyxl.load_workbook(file_path, read_only=True)
        ws = wb.active
        rows = list(ws.iter_rows(min_row=1, max_row=1, values_only=True))
        if rows:
            print(f"Header: {rows[0]}")
        else:
            print("File is empty")
    except Exception as e:
        print(f"Error: {e}")
else:
    print(f"File not found: {file_path}")
