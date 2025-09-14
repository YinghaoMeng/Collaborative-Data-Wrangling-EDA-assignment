# Homework #3: Collaborative Data Wrangling & EDA
Yinghao Meng

This project focuses on **data wrangling and exploratory data analysis (EDA)** using real-world supermarket datasets.  
The workflow includes:  
- Dataset integration and cleaning  
- Missing value imputation  
- Outlier detection and removal  
- Processed dataset generation

## 1.	Dataset Information
The data used in this project is sourced from Problem C of [The 2023 China National College Students Mathematical Modeling Competition](https://dxs.moe.gov.cn/zx/a/hd_sxjm_sthb/230523/1840580.shtml) . All data involved is publicly available dataset, comprising four sub-datasets: 
The dataset includes four files:

1.1. **Attachment 1.xlsx** – Product information for six vegetable categories sold at a Chinese supermarket. (13.7KB, 252 rows)  
   - Item Code  
   - Classification Code  
   - Classification Name  

1.2. **Attachment 2.xlsx** – Sales transaction details for each product at this supermarket from July 1, 2020, to June 30, 2023. (36.9MB, 878540 rows)  
   - Sales Date  
   - Scan-to-Buy Time  
   - Item Code  
   - Sales Volume (kg)  
   - Sales Unit Price (CNY/kg)  
   - Sales Type  
   - Discount availability  

1.3. **Attachment 3.xlsx** – Wholesale Prices for Various Products at this supermarket from July 1, 2020, to June 30, 2023. (1.09MB, 55983 rows)  
   - Date  
   - Item Code  
   - Wholesale Price (CNY/kg)  

1.4. **Attachment 4.xlsx** – Recent wastage rate data for various products at this supermarket. (14.8KB, 252 rows)  
   - Item Code  
   - Wastage Rate (%)  

---
## 2.	Contribution Record

2.1. **Standardize & Merge**
- Normalize column names and key columns (e.g., Item Code, Date)
- For Item Code, cast to string and strip suffix like .0
- De-duplicate per table; keep one row per Item Code where appropriate
- Merge tables: Attachment 2 (sales) ← left join Attachment 1/3/4 by Item Code

2.2. **Missing Values**
- Date-like columns: forward-fill then back-fill  
- Numeric columns: median fill  
- Categorical columns: mode (fallback to "Unknown")

3.3. **Outliers (3σ)**
- For each numeric column, flag values outside [mean − 3σ, mean + 3σ]
- Remove flagged rows; export removed rows and thresholds summary

3.4. **Outputs**
- **Merged_Table.xlsx** — New table created by merging Tables 1, 3, and 4 into Table 2 and removing duplicate values. (48.7MB, 878504 rows)
- **Merged_Table_filled.xlsx** — New table after filling in missing values. (48.7MB, 878504 rows. Note: There are no missing values in the merged table.)
- **Merged_Table_3sigma_cleaned.xlsx** — New table after handling outliers. (57.3MB, 851425 rows)
- **Removed_Rows_3sigma.xlsx** — Abnormal data summary table. (1.77MB, 27080 rows)
- **Three_Sigma_Thresholds.xlsx** — Summary table of thresholds for each column calculated using the 3σ principle.



------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Homework #3: Collaborative Data Wrangling \& EDA
DSE 511 – Fall 2025



Exploratory Data Analysis (EDA):  (Tahmid)



Descriptive Statistics:

1\. Sales Dates range from 2020-07-01 to 2023-06-30 indicating dataset spans about 3 years of transactions.



2\. Item Code / Classification Codes are large numeric identifiers which means that the Mean/std not really useful here as they’re IDs, not continuous variables.



3\. Sales Volume (kg)



Mean: ~0.53 kg per transaction.

Median (50%): 0.43 kg → most sales are small quantities.

Range: -0.66 to 1.73 kg

Negative values likely mean indicate returns.





4\. Sales Unit Price (CNY/kg)



Mean: 8.51 CNY/kg.

Median: 7.6 CNY/kg.

Range: 0.1 to 27.8 CNY/kg Indicating Very wide spread hence different product categories.



5\. Wholesale Price (CNY/kg)



Mean: 6.02 CNY/kg.

Median: 4.62 CNY/kg.

Range: 0.01 to 16 CNY/kg.

Wholesale is consistently lower than sales price (as expected).





6\. Wastage Rate (%)



Mean: 9.88%.

Median: 9.4%.

Range: 0 to 22.7%.

Some products waste more, could signal perishable items.



Visualizations:



Histograms



Sales Volume: Right-skewed, most sales clustered at lower quantities.

Sales Price: Highly variable, with multiple peaks indicating product clusters.

Wholesale Price: More stable distribution, fewer extreme values.



Boxplots



Sales Type vs Volume:

Sold items have higher variability and clear outliers. Returns are consistently lower with tighter distribution. Boxplots highlighted significant outliers in sales volume.



Time-Series Analysis



Sales Price (blue) vs Wholesale Price (orange):

Retail sales prices are volatile, with seasonal peaks (start of 2021, 2022, 2023). Wholesale prices are smoother and less volatile. The margin (Sales – Wholesale) fluctuates, widening during spikes but tightening at times.

 main
