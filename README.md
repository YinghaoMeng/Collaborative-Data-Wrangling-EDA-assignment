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

