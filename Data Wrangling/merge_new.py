import pandas as pd

# ====== 文件名 ======
F1 = "Attachment 1.xlsx"  # 分类（右表）
F2 = "Attachment 2.xlsx"  # 销售（主表）
F3 = "Attachment 3.xlsx"  # 批发价（右表）
F4 = "Attachment 4.xlsx"  # 损耗率（右表）
OUTPUT = "Merged_Table.xlsx"

# ====== 1. 清洗列名：转字符串 + 去首尾空格 ======
def clean_column_names(df):
    cols = df.columns.astype(str)
    df.columns = cols.str.strip()
    return df

# ====== 2. 统一关键列名（把常见别名改成标准名）======
def unify_key_names(df):
    # 主键列：统一叫 "Item Code"
    key_alias = ["ItemCode", "ITEM CODE", "item code"]
    if "Item Code" not in df.columns:
        for name in key_alias:
            if name in df.columns:
                df.rename(columns={name: "Item Code"}, inplace=True)
                break
    # 日期列：统一叫 "Date"（如果有）
    date_alias = ["date", "Date "]
    if "Date" not in df.columns:
        for name in date_alias:
            if name in df.columns:
                df.rename(columns={name: "Date"}, inplace=True)
                break
    return df

# ====== 3. 清洗 Item Code 数据：转字符串、去空格、去掉结尾“.0” ======
def clean_item_code(series):
    series = series.astype(str)
    series = series.str.strip()
    series = series.str.replace(r"\.0$", "", regex=True)
    return series

# ====== 4. 让每个 Item Code 只保留一条（可选先按日期排序）======
def keep_one_row_per_item(df, key="Item Code", keep="last", sort_by=None):
    if sort_by is not None and sort_by in df.columns:
        df = df.sort_values(by=sort_by)
    df = df.drop_duplicates(subset=[key], keep=keep)
    return df

# ====== 读取四张表（默认读 Sheet1；若你的表不是 Sheet1，请改成对应的 sheet_name）======
t1 = pd.read_excel(F1, sheet_name="Sheet1")
t2 = pd.read_excel(F2, sheet_name="Sheet1")
t3 = pd.read_excel(F3, sheet_name="Sheet1")
t4 = pd.read_excel(F4, sheet_name="Sheet1")

# ====== 清洗列名 + 统一关键列名 ======
for df in (t1, t2, t3, t4):
    clean_column_names(df)
    unify_key_names(df)

# ====== 统一 Item Code 的数据格式 ======
for df in (t1, t2, t3, t4):
    df["Item Code"] = clean_item_code(df["Item Code"])

# ====== 右表去重（避免多对多）======
# 表1：分类 → 同一 Item Code 只保留第一条
t1_u = keep_one_row_per_item(t1, key="Item Code", keep="first")

# 表3：批发价 → 如果有 Date，就按日期排好后保留“最新”；没有就直接保留最后一条
if "Date" in t3.columns:
    t3["Date"] = pd.to_datetime(t3["Date"], errors="coerce")
    t3 = t3.sort_values(by="Date")
t3_u = keep_one_row_per_item(t3, key="Item Code", keep="last")

# 表4：损耗率 → 同一 Item Code 只保留最后一条
t4_u = keep_one_row_per_item(t4, key="Item Code", keep="last")

# ====== 合并到表2（主表）======
merged = pd.merge(t2, t1_u, on="Item Code", how="left", suffixes=("", "_cls"))
merged = pd.merge(merged, t3_u, on="Item Code", how="left", suffixes=("", "_whl"))
merged = pd.merge(merged, t4_u, on="Item Code", how="left", suffixes=("", "_wst"))

# ====== 导出并打印覆盖率 ======
merged.to_excel(OUTPUT, index=False)
print(f"合并完成：{OUTPUT}")

n_all = len(t2)
n1 = merged["Item Code"].isin(t1_u["Item Code"]).sum()
n3 = merged["Item Code"].isin(t3_u["Item Code"]).sum()
n4 = merged["Item Code"].isin(t4_u["Item Code"]).sum()
print(f"[覆盖率] 表1: {n1}/{n_all}，表3: {n3}/{n_all}，表4: {n4}/{n_all}")