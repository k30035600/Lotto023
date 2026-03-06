import openpyxl
import os

file_path = r'source/Lotto645.xlsx'

if os.path.exists(file_path):
    try:
        wb = openpyxl.load_workbook(file_path, read_only=True)
        ws = wb.active
        
        rows = list(ws.iter_rows(values_only=True))
        
        if not rows:
            print("File is empty")
        else:
            header = rows[0]
            first_data = rows[1] if len(rows) > 1 else None
            last_data = rows[-1] if len(rows) > 1 else None
            
            print(f"Header: {header}")
            print(f"First Data Row (Row 2): {first_data}")
            print(f"Last Data Row (Row {len(rows)}): {last_data}")
            
    except Exception as e:
        print(f"Error reading file: {e}")
else:
    print(f"File not found: {file_path}")
