import pandas as pd

df = pd.read_excel("Merged_Table.xlsx")
# Search for the numerical column to be checked
num_cols = ["Sales Volume (kilograms)","Sales Unit Price (CNY/kg)","Wholesale Price (CNY/kg)","Wastage Rate (%)"]

# Ensure these columns are of the “numeric type”.
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Identify abnormalities using the 3σ principle:
# values less than (mean - 3*standard deviation) or greater than (mean + 3*standard deviation)
thresholds = []
rows_to_drop = set()

for col in num_cols:
    mu = df[col].mean() #mean
    sd = df[col].std() #standard deviation
    lower = mu - 3 * sd
    upper = mu + 3 * sd
    is_outlier = (df[col] < lower) | (df[col] > upper)
    outlier_indices = df.index[is_outlier]
    print(f"{col}：Mean={mu:.4f}，Standard Deviation={sd:.4f}，Lower Bound={lower:.4f}，Upper Bound={upper:.4f}，Number of Outliers={len(outlier_indices)}")
    thresholds.append({
        "column": col,
        "mean": mu,
        "std": sd,
        "lower": lower,
        "upper": upper,
        "n_outliers": int(len(outlier_indices))
    })
    rows_to_drop.update(outlier_indices)

if len(rows_to_drop) > 0:
    removed = df.loc[list(rows_to_drop)]
else:
    removed = pd.DataFrame(columns=df.columns)

# Delete these rows to obtain clean data.
cleaned = df.drop(index=rows_to_drop)
removed.to_excel("removed_rows_3sigma.xlsx", index=False)
cleaned.to_excel("Merged_Table_3sigma_cleaned.xlsx", index=False)
pd.DataFrame(thresholds).to_excel("three_sigma_thresholds.xlsx", index=False)
print(f"Number of rows deleted：{len(rows_to_drop)}")