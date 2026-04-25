# 🚀 Vendor Performance Analysis

## 💡 Business Problem
Businesses often face high inventory costs and reduced profitability due to lack of visibility into vendor performance.

This project analyzes vendor sales and inventory data to identify inefficiencies, optimize vendor selection, and reduce capital locked in unsold inventory.

---

## 💰 Key Business Impact

- Identified **₹2.71 Million in unsold inventory (locked capital)**
- Discovered **low-performing vendors with higher margins (41.57%) vs top vendors (31.18%)**
- Highlighted **overstocking risks from major vendors contributing ₹700K+ each**
- Enabled data-driven strategies to improve procurement and profitability

---

## 📊 Approach

- Data Cleaning & Transformation using Python & SQL  
- Exploratory Data Analysis (EDA)  
- KPI Calculation:
  - Profit Margin  
  - Stock Turnover  
  - Sales-to-Purchase Ratio  
- Vendor Segmentation (Top vs Low)  
- Statistical Hypothesis Testing (T-Test, 95% Confidence Interval)

---

## 🔍 Key Insights

### 📦 Inventory Risk
- Total unsold capital: **₹2.71M**
- Major contributors:
  - DIAGEO NORTH AMERICA INC — ₹722K+
  - JIM BEAM BRANDS — ₹554K+
  - PERNOD RICARD — ₹470K+

👉 Indicates over-purchasing and poor inventory planning

---

### 📈 Profitability Analysis
- Low-performing vendors: **41.57% margin**
- Top vendors: **31.18% margin**

👉 Opportunity for vendor rebalancing and margin renegotiation

---

### 🔄 Sales Efficiency
- Stock turnover: ~0.97–0.99  
- Sales-to-purchase ratio: ≥ 1.30  

👉 Moderate efficiency with room for optimization

---

### 🧪 Statistical Validation
- T-Test shows significant difference in margins (**p < 0.001**)  
- Confirms insights are statistically reliable  

---

## 🧠 Business Recommendations

- Reduce закуп from vendors with high unsold inventory  
- Prioritize high-margin vendors  
- Renegotiate contracts with large vendors  
- Optimize inventory planning  
- Implement demand forecasting  

---

## 🛠️ Tools & Technologies

- Python (Pandas, NumPy)  
- SQL  
- Matplotlib, Seaborn  
- SciPy  
- Jupyter Notebook  

---

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
