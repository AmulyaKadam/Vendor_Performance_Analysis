# 🌟 Vendor Performance Analysis

A complete **ETL + EDA + Statistical Analysis** project focused on understanding vendor performance, profitability, inventory movement, and unsold capital.  
This project helps businesses **optimize vendor relationships**, **reduce capital lock**, and **identify high-margin opportunities**.

## 📁 Project Structure
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

## 🚀 Project Overview

This project performs:

- 🔹 **ETL** – Loading, cleaning, transforming vendor sales data  
- 🔹 **Descriptive Analytics** – Sales, purchases, margins, turnovers  
- 🔹 **Inventory Analysis** – Unsold inventory & capital lock calculations  
- 🔹 **Vendor Classification** – Top vs. Low vendor segmentation  
- 🔹 **Statistical Testing** – Confidence intervals & T-test  
- 🔹 **Business Insights** – Profitability, efficiency & strategic recommendations  

---

# 📊 Detailed Insights Overview

## 🧮 1. Vendor-Level KPI Summary

| KPI | Example Values |
|-----|----------------|
| **Profit Margin** | 21.06%, 24.67%, 27.14%, 28.41% |
| **Stock Turnover** | 0.976, 0.993, 0.999, 0.984 |
| **Sales-to-Purchase Ratio** | 1.266, 1.338, 1.372, 1.397 |
| **Gross Profit** | ₹1,015,032 → ₹1,299,667 → ₹1,194,774 |

---

## 📦 2. Unsold Inventory Analysis

### 💰 Total Unsold Capital Locked: **₹ 2.71 Million**

Top vendors contributing the most:

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

---

## 📈 3. Profitability Comparison (Top vs Low Vendors)

- **Top Vendors Mean Margin:** 31.18%  
- **Low Vendors Mean Margin:** 41.57%  
- **95% CI (Top):** 30.74% – 31.61%  
- **95% CI (Low):** 40.50% – 42.64%  

---

## 🧪 4. Statistical T-Test

- **T-Statistic:** −17.6693  
- **P-Value:** 0.0000  
- **Conclusion:** Significant difference in profit margins.

---

## 🔄 5. Stock Turnover & Sales Efficiency

- Turnover ratios: ~0.97–0.99  
- Sales-to-purchase ratio: ≥ 1.30  

---

# 🧠 Strategic Recommendations

- 🌱 Expand high-margin vendors  
- 🔻 Reduce over-purchasing from high unsold-inventory vendors  
- 🔄 Improve demand forecasting  
- 💹 Renegotiate margins with large vendors  
- 📦 Analyze SKU-level performance  

---

# 🛠️ Technologies Used

- 🐍 Python  
- 📓 Jupyter Notebook  
- 🗄️ SQL  
- 📊 Pandas, NumPy  
- 📉 Matplotlib, Seaborn  
- 🧮 SciPy  

---

# 📜 Future Enhancements

- Time-series demand forecasting  
- Vendor scoring model  
- Dashboard creation  
- Automated ETL pipeline  

---

# 🤝 Contributing

1. Fork this repository  
2. Create a new branch  
3. Commit your changes  
4. Submit a pull request  

---

# 📬 Contact
**Amulya Kadam**  
📧 kadamamulya017@gmail.com  
🔗 LinkedIn: www.linkedin.com/in/amulya-kadam-8b3647208 
