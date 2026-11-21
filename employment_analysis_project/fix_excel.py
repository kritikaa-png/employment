
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

input_file = "data/synthetic_employment_salary_dataset.xlsx"
output_file = "data/employment_dataset_clean.xlsx"

# Read Excel dataset
df = pd.read_excel(input_file, sheet_name="Dataset")

# Clean column names
df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.replace(" ", "_")
)

# Clean text columns
for col in df.select_dtypes(include="object").columns:
    df[col] = (
        df[col].astype("string")
        .str.replace("\u00a0", " ", regex=False)
        .str.strip()
    )

# Ensure salary is numeric
df["Annual_Salary_INR"] = pd.to_numeric(
    df["Annual_Salary_INR"], errors="coerce"
)

# Create clean Excel file
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Dataset", index=False)

    dictionary = pd.DataFrame({
        "Column": df.columns,
        "Data_Type": [str(df[c].dtype) for c in df.columns],
        "Description": [
            "Synthetic employment analysis field"
            for c in df.columns
        ]
    })
    dictionary.to_excel(
        writer, sheet_name="Data_Dictionary", index=False
    )

# Apply professional formatting
wb = load_workbook(output_file)

for ws in wb.worksheets:
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    ws.sheet_view.showGridLines = False

    for cell in ws[1]:
        cell.font = Font(
            name="Arial",
            bold=True,
            color="FFFFFF",
            size=11
        )
        cell.fill = PatternFill(
            "solid", fgColor="17365D"
        )
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

    ws.row_dimensions[1].height = 28

    for column in ws.columns:
        letter = column[0].column_letter
        max_length = max(
            len(str(c.value)) if c.value is not None else 0
            for c in column[:500]
        )
        ws.column_dimensions[letter].width = min(
            max(max_length + 3, 14), 35
        )

# Format salary column
ws = wb["Dataset"]
headers = {cell.value: cell.column for cell in ws[1]}

if "Annual_Salary_INR" in headers:
    col = headers["Annual_Salary_INR"]
    for row in range(2, ws.max_row + 1):
        ws.cell(row, col).number_format = '#,##0'

wb.save(output_file)

print("Excel file cleaned successfully!")
print("Saved to:", output_file)
print("Total records:", len(df))
