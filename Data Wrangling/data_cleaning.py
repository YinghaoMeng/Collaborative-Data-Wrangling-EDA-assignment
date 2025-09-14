import pandas as pd

# 1) 读数据
df = pd.read_excel("Merged_Table.xlsx")

# 2) ——缺失值检测（在哪里缺？缺多少？）——
print("每一列的缺失值个数：")
print(df.isnull().sum())  # 按列统计缺失个数

for col in df.columns:
    col_lower = str(col).lower()

    # 3.1 日期列（按列名判断）
    if "date" in col_lower:
        df[col] = df[col].fillna(method="ffill")  # 用前一个非空值补
        df[col] = df[col].fillna(method="bfill")  # 还空的话，用后一个非空值补

    # 3.2 数字列（用中位数）
    elif df[col].dtype in ["int64", "float64"]:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)

    # 3.3 文本/分类列（用众数；没有就 Unknown）
    else:
        mode_vals = df[col].mode()
        if len(mode_vals) > 0:
            fill_val = mode_vals[0]
        else:
            fill_val = "Unknown"
        df[col] = df[col].fillna(fill_val)

# 4) 再检查一次缺失是否都补好了
print("填补后每一列的缺失值个数：")
print(df.isnull().sum())

# 5) 导出结果
df.to_excel("Merged_Table_filled.xlsx", index=False)
print("处理完成：Merged_Table_filled.xlsx（数据） + missing_report.xlsx（缺失位置清单）")
