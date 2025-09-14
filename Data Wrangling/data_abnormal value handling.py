import pandas as pd

# 1) 读数据
df = pd.read_excel("Merged_Table.xlsx")

# 2) 要检查的数值列（有些表可能缺列，先过滤一遍）
num_cols = ["Sales Volume (kilograms)","Sales Unit Price (CNY/kg)","Wholesale Price (CNY/kg)","Wastage Rate (%)"]

# 3) 确保这些列是“数字类型”（如果不是，就强制转一下；转不动的会变成 NaN）
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 4) 用 3σ 原则找异常：小于 (均值-3*标准差) 或 大于 (均值+3*标准差)
#    记录每列的阈值和被判定为异常的行
thresholds = []         # 记录阈值，方便导出
rows_to_drop = set()    # 所有需要删除的行索引（只要任一列是异常，就删整行）

for col in num_cols:
    mu = df[col].mean(skipna=True)   # 均值
    sd = df[col].std(skipna=True)    # 标准差

    lower = mu - 3 * sd
    upper = mu + 3 * sd

    # 这一列哪些行是异常
    is_outlier = (df[col] < lower) | (df[col] > upper)
    outlier_indices = df.index[is_outlier & df[col].notna()]  # 只对非空的数值判断

    # 打印一下统计
    print(f"{col}：均值={mu:.4f}，标准差={sd:.4f}，下界={lower:.4f}，上界={upper:.4f}，异常行数={len(outlier_indices)}")

    # 记录阈值和异常数量
    thresholds.append({
        "column": col,
        "mean": mu,
        "std": sd,
        "lower": lower,
        "upper": upper,
        "n_outliers": int(len(outlier_indices))
    })

    # 累积需要删除的行
    rows_to_drop.update(outlier_indices.tolist())

# 5) 导出被删除的异常行，和删除后的干净数据
removed = df.loc[sorted(rows_to_drop)].copy() if len(rows_to_drop) > 0 else pd.DataFrame(columns=df.columns)
cleaned = df.drop(index=rows_to_drop)

removed.to_excel("removed_rows_3sigma.xlsx", index=False)
cleaned.to_excel("Merged_Table_3sigma_cleaned.xlsx", index=False)
pd.DataFrame(thresholds).to_excel("three_sigma_thresholds.xlsx", index=False)

print("完成 3σ 异常值处理：")
print(f" - 删除行数：{len(rows_to_drop)}")
print(" - 已导出：Merged_Table_3sigma_cleaned.xlsx（删除异常后的数据）")
print(" - 已导出：removed_rows_3sigma.xlsx（被删掉的异常行明细）")
print(" - 已导出：three_sigma_thresholds.xlsx（各列的均值、标准差、阈值、异常数量）")
