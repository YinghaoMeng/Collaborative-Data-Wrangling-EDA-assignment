import pandas as pd

df = pd.read_excel("Merged_Table.xlsx")

# Detection of missing value locations and quantities
print("Number of missing values in each column:")
print(df.isnull().sum())

# Iterate through each column, convert the column names to strings first, then convert them all to lowercase.
# Different filling methods are provided for different types of missing data.
for col in df.columns:
    col_lower = str(col).lower()
    if "date" in col_lower:
        df[col] = df[col].fillna(method="ffill")
        df[col] = df[col].fillna(method="bfill")
    elif df[col].dtype in ["int64", "float64"]:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
    else:
        mode_vals = df[col].mode()
        if len(mode_vals) > 0:
            fill_val = mode_vals[0]
        else:
            fill_val = "Unknown"
        df[col] = df[col].fillna(fill_val)

print("Number of missing values in each column after filling:")
print(df.isnull().sum())
df.to_excel("Merged_Table_filled.xlsx", index=False)
print(f"DONE：Merged_Table_filled.xlsx")