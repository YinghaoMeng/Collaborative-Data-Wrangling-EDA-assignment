import pandas as pd
from pathlib import Path

# ========= 配置 =========
FILE1 = "Attachment 1.xlsx"  # 分类
FILE2 = "Attachment 2.xlsx"  # 销售（主表）
FILE3 = "Attachment 3.xlsx"  # 批发价（可能含日期）
FILE4 = "Attachment 4.xlsx"  # 损耗率
OUT   = "Merged_Table.xlsx"

# ========= 工具函数 =========
#def best_sheet_name(xls: pd.ExcelFile, prefer="Sheet1"):
#    """优先返回 Sheet1，否则返回第一个工作表名"""
#    if prefer in xls.sheet_names:
#        return prefer
#  return xls.sheet_names[0]

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.map(lambda c: str(c).strip())
    return df

def find_item_code_column(df: pd.DataFrame) -> str:
    cols = [c.strip() for c in df.columns.astype(str)]
    # 1) 直接命中
    if "Item Code" in cols:
        return "Item Code"
    # 2) 常见别名
    alias = {
        "商品编码": "Item Code",
        "item code": "Item Code",
        "ITEM CODE": "Item Code",
        "ItemCode": "Item Code",
        "商品代碼": "Item Code",
        "Item_ID": "Item Code",
        "Item Id": "Item Code",
        "Item id": "Item Code",
        "条码": "Item Code",
        "Barcode": "Item Code",
        "SKU": "Item Code",
    }
    for old, new in alias.items():
        if old in cols:
            df.rename(columns={old: new}, inplace=True)
            return "Item Code"
    # 3) 模糊匹配：列名里同时包含 item 和 code 或 包含 编码/条码/SKU
    for c in cols:
        lc = c.lower()
        if ("item" in lc and "code" in lc) or ("编码" in c) or ("條碼" in c) or ("条码" in c) or ("sku" in lc):
            df.rename(columns={c: "Item Code"}, inplace=True)
            return "Item Code"
    raise KeyError(f"未找到主键列：Item Code；当前列名：{cols}")

def normalize_item_code(series: pd.Series) -> pd.Series:
    s = series.astype(str).str.strip()
    # 去除 Excel 浮点读入的尾部 .0
    s = s.str.replace(r"\.0$", "", regex=True)
    return s

def ensure_unique_by_key(df: pd.DataFrame, key: str, keep="last", sort_by=None):
    """让右表按 key 唯一；若提供 sort_by，先排序再去重"""
    if sort_by is not None:
        df = df.sort_values(sort_by)
    dup = df.duplicated(subset=[key], keep=False)
    if dup.any():
        n = dup.sum()
        print(f"[Info] 发现 {n} 行 {key} 重复，将通过 drop_duplicates 保留 {keep}.")
    return df.drop_duplicates(subset=[key], keep=keep)

def minimal_right(df: pd.DataFrame, key: str, keep_cols=None):
    """只保留用于合并的必要列，降低内存占用"""
    if keep_cols is None:
        # 默认保留 key + 非重复信息列（排除完全重复的列名）
        keep_cols = [c for c in df.columns if c != key]
    # 始终把 key 放最前
    cols = [key] + [c for c in keep_cols if c != key]
    # 去重列名（防用户重复列）
    seen, final_cols = set(), []
    for c in cols:
        if c not in seen and c in df.columns:
            final_cols.append(c)
            seen.add(c)
    return df[final_cols]

# ========= 读取工作表 =========
xf1, xf2, xf3, xf4 = (pd.ExcelFile(FILE1), pd.ExcelFile(FILE2), pd.ExcelFile(FILE3), pd.ExcelFile(FILE4))
#sh1, sh2, sh3, sh4 = (best_sheet_name(xf1), best_sheet_name(xf2), best_sheet_name(xf3), best_sheet_name(xf4))

t1 = pd.read_excel(xf1, sheet_name=sh1)
t2 = pd.read_excel(xf2, sheet_name=sh2)
# 表3可能有日期列，先不强制 parse，后面再判断
t3 = pd.read_excel(xf3, sheet_name=sh3)
t4 = pd.read_excel(xf4, sheet_name=sh4)

# ========= 规范列名 & 主键 =========
for df in (t1, t2, t3, t4):
    normalize_columns(df)
for df in (t1, t2, t3, t4):
    key = find_item_code_column(df)  # 会就地重命名为 "Item Code"

# 统一键类型
for df in (t1, t2, t3, t4):
    df["Item Code"] = normalize_item_code(df["Item Code"])

# ========= 右表去重策略 =========
# 表1（分类）：每 Item Code 一行，保留首次出现
t1_u = ensure_unique_by_key(t1, key="Item Code", keep="first")

# 表3（批发价）：如含 Date/日期，按时间排序后保留“最新”
date_col = None
for cand in ["Date", "日期", "date"]:
    if cand in t3.columns:
        date_col = cand
        break
if date_col:
    # 尝试转日期
    t3[date_col] = pd.to_datetime(t3[date_col], errors="coerce")
    t3_u = ensure_unique_by_key(t3, key="Item Code", keep="last", sort_by=date_col)
else:
    t3_u = ensure_unique_by_key(t3, key="Item Code", keep="last")

# 表4（损耗率）：每 Item Code 一行，保留最后出现
t4_u = ensure_unique_by_key(t4, key="Item Code", keep="last")

# ========= 精简右表列，降低内存 =========
t1_u = minimal_right(t1_u, key="Item Code")
t3_u = minimal_right(t3_u, key="Item Code")
t4_u = minimal_right(t4_u, key="Item Code")

# ========= 合并（m:1 安全校验）=========
merged = pd.merge(t2, t1_u, on="Item Code", how="left", validate="m:1", suffixes=("", "_cls"))
merged = pd.merge(merged, t3_u, on="Item Code", how="left", validate="m:1", suffixes=("", "_whl"))
merged = pd.merge(merged, t4_u, on="Item Code", how="left", validate="m:1", suffixes=("", "_wst"))

# ========= 输出 =========
merged.to_excel(OUT, index=False)
print(f"✅ 合并完成：{OUT}")

# ========= 诊断信息（可选）=========
n_all = len(t2)
n1 = merged["Item Code"].isin(t1_u["Item Code"]).sum()
n3 = merged["Item Code"].isin(t3_u["Item Code"]).sum()
n4 = merged["Item Code"].isin(t4_u["Item Code"]).sum()
print(f"[覆盖率] 表1: {n1}/{n_all}，表3: {n3}/{n_all}，表4: {n4}/{n_all}")
