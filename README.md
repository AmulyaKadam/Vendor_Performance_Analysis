# Vendor Performance Analysis
A complete ETL + EDA project analyzing vendor performance, profitability, inventory movement, and unsold capital using Python and SQL.

## Repository Structure
```
Vendor_Performance_Analysis/
├── Jupyter Notebook/
│   ├── vendor_performance_analysis (2).ipynb
│   └── Vendor_performance_analysis_EDA.ipynb
├── Python Scripts/
│   ├── etl.py
│   └── utils.py
├── dataset/
│   └── vendor_sales.csv
├── logs/
│   └── etl.log
└── README.md
```

## Detailed Insights Overview (With Actual Extracted Values)

### 1. Vendor-Level KPI Summary
Your analysis computed KPIs such as Gross Profit, Profit Margin, Stock Turnover Ratio, and Sales-to-Purchase Ratio.

Example values:
- Profit Margin: 21.06%, 24.67%, 27.14%, 28.41%
- Stock Turnover: 0.976, 0.993, 0.999, 0.984
- Sales-to-Purchase Ratio: 1.266, 1.338, 1.372, 1.397
- Gross Profit: ₹1,015,032 → ₹1,299,667 → ₹1,194,774

### 2. Unsold Inventory Analysis
- **Total Unsold Capital: ₹2.71 Million**

Top vendors by unsold inventory:
- DIAGEO NORTH AMERICA INC — ₹722.21K
- JIM BEAM BRANDS COMPANY — ₹554.67K
- PERNOD RICARD USA — ₹470.63K
- WILLIAM GRANT & SONS INC — ₹401.96K
- E & J GALLO WINERY — ₹228.28K
- SAZERAC CO INC — ₹198.44K
- BROWN-FORMAN CORP — ₹177.73K
- CONSTELLATION BRANDS INC — ₹133.62K
- MOET HENNESSY USA INC — ₹126.48K
- REMY COINTREAU USA INC — ₹118.60K

### 3. Profitability Comparison: Top vs Low Vendors
Top Vendors:
- 95% CI: (30.74%, 31.61%)
- Mean Profit Margin: 31.18%

Low Vendors:
- 95% CI: (40.50%, 42.64%)
- Mean Profit Margin: 41.57%

### 4. Statistical Test
- T-Statistic: -17.6693
- P-Value: 0.0000
- Conclusion: Significant difference in profit margins.

### 5. Stock Turnover & Sales Efficiency
- Turnover: ~0.97–0.99
- Sales-to-Purchase Ratio: ≥1.30

### 6. Vendor Contribution Insights
- Large vendors dominate purchases but also unsold stock.
- Smaller vendors offer higher profit margins (>40%).

### 7. Strategic Insights
- Prioritize high-margin vendors.
- Reduce excess purchasing from large vendors with high unsold inventory.
- Improve forecasting and stock planning.
