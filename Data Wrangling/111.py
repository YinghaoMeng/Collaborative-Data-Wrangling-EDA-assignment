import pandas as pd

F1 = "Attachment 1.xlsx"
F2 = "Attachment 2.xlsx"
F3 = "Attachment 3.xlsx"
F4 = "4_Test.xlsx"
OUTPUT = "Merged_Table_Test.xlsx"

t1 = pd.read_excel(F1)
t2 = pd.read_excel(F2)
t3 = pd.read_excel(F3)
t4 = pd.read_excel(F4)

# Perform forced conversion of the first row (column names) in the four tables to strings.
# And standardize the key column names.
for df in (t1, t2, t3, t4):
    cols = df.columns.astype(str)
    df.columns = cols.str.strip()
    # ### FIX: 扩充别名，命中率更高
    key_alias = ["ItemCode", "ITEM CODE", "item code"]
    if "Item Code" not in df.columns:
        for name in key_alias:
            if name in df.columns:
                df.rename(columns={name: "Item Code"}, inplace=True)
                break

    date_alias = ["date", "Date "]
    if "Date" not in df.columns:
        for name in date_alias:
            if name in df.columns:
                df.rename(columns={name: "Date"}, inplace=True)
                break

    # ### FIX: 只有在确实存在 'Item Code' 时才做清洗，避免 KeyError
    if "Item Code" in df.columns:
        df["Item Code"] = df["Item Code"].astype(str)
        df["Item Code"] = df["Item Code"].str.strip()
        df["Item Code"] = df["Item Code"].str.replace(r"\.0$", "", regex=True)

# ### FIX: 强校验——到这一步还没有 'Item Code' 就直接报清晰错误
for i, df in enumerate((t1, t2, t3, t4), start=1):
    if "Item Code" not in df.columns:
        raise KeyError(f"表{i} 缺少列 'Item Code'。当前列名：{list(df.columns)}")

# For each Item Code in the table, only one corresponding row of data is retained.
# Reminder: This is a FUNCTION.
def keep_one_row_per_item(df, key="Item Code", keep="last", sort_by=None):
    if sort_by is not None and sort_by in df.columns:
        df = df.sort_values(by=sort_by)
    df = df.drop_duplicates(subset=[key], keep=keep)
    return df

t1_u = keep_one_row_per_item(t1, key="Item Code", keep="first")

# ### FIX: 只有有 'Date' 列才做 to_datetime+排序；否则直接跳过，避免 KeyError
if "Date" in t3.columns:
    t3["Date"] = pd.to_datetime(t3["Date"], errors="coerce")
    t3 = t3.sort_values(by="Date")
t3_u = keep_one_row_per_item(t3, key="Item Code", keep="last")

t4_u = keep_one_row_per_item(t4, key="Item Code", keep="last")

# Merge Tables 1, 3, and 4 into Table 2.
merged = pd.merge(t2, t1_u, on="Item Code", how="left", suffixes=("", "_cls"))
merged = pd.merge(merged, t3_u, on="Item Code", how="left", suffixes=("", "_whl"))
merged = pd.merge(merged, t4_u, on="Item Code", how="left", suffixes=("", "_wst"))

merged.to_excel(OUTPUT, index=False)
print(f"DONE：{OUTPUT}")

n_all = len(t2)
n1 = merged["Item Code"].isin(t1_u["Item Code"]).sum()
n3 = merged["Item Code"].isin(t3_u["Item Code"]).sum()
n4 = merged["Item Code"].isin(t4_u["Item Code"]).sum()
print(f"[Completion rate] Table 1: {n1}/{n_all}，Table 3: {n3}/{n_all}，Table 4: {n4}/{n_all}")
