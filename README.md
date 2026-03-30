# 📊 Olist Data Engineering Pipeline

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-black?logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-orange?logo=numpy)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Focus](https://img.shields.io/badge/Focus-Data%20Engineering-blueviolet)

---

## 🚀 Project Summary
End-to-end **data pipeline** that transforms raw Brazilian e-commerce data (Olist) into a **star schema model** ready for analytics and **Power BI dashboards**.

✔️ Data ingestion  
✔️ Data cleaning & transformation  
✔️ Feature engineering  
✔️ Dimensional modeling (Star Schema)  
✔️ KPI generation  
✔️ Export for BI tools  

---

## 🧱 Project Structure

data/ 

├── raw/  
├── processed/  

src/

└── pipeline.py 

---

## ⚙️ Tech Stack

- Python  
- Pandas  
- NumPy  
- ETL Pipeline Design  
- Dimensional Modeling  

---

## 🔄 Pipeline Overview

### 📥 Ingestion
Loads multiple datasets:
- Orders  
- Order Items  
- Customers  
- Products  
- Sellers  
- Payments  
- Reviews  

---

### 🧹 Data Processing
- Datetime standardization  
- Type casting (categorical & numeric)  
- Data consistency checks  
- Handling missing values  

---

### 🧱 Data Modeling

**Star Schema Design**

**Dimension Tables**
- dim_customer  
- dim_product  
- dim_seller  

**Fact Tables**
- fact_orders  
- fact_payments  
- fact_reviews  

---

### ⚡ Feature Engineering
- order_value = price + freight  
- delivery_time  
- delivery_delay  
- purchase_month  

---

### 📊 KPIs Generated
- Total Revenue  
- Total Orders  
- Average Ticket Size  
- Cancellation Rate  
- Average Delivery Time  
- Delivery Delay  
- Repeat Customer Rate  
- Revenue by Category  

---

## 📤 Output Data

data/processed/
 ├── clean_olist.csv  
 ├── olist_dim_customer.csv  
 ├── olist_dim_product.csv  
 ├── olist_dim_seller.csv  
 ├── olist_fact_orders.csv  
 ├── olist_fact_payments.csv  
 ├── olist_fact_reviews.csv  
 └── backup_main_df.csv  

---

## ▶️ How to Run

### 1. Clone the repository
git clone https://github.com/your-username/your-repo.git  
cd your-repo  

### 2. Install dependencies
pip install -r requirements.txt  

### 3. Run the pipeline
python src/pipeline.py  

---

## 📈 Business Value
- Provides ready-to-use datasets for BI tools  
- Enables fast dashboard creation in Power BI  
- Demonstrates a real-world data engineering workflow  

---

## 🧠 Key Skills Demonstrated
- End-to-end data pipeline development  
- Data cleaning and transformation at scale  
- Dimensional data modeling (Star Schema)  
- Writing clean, production-style Python code  

---

## 🔮 Future Improvements
- Cloud Data Warehouse (BigQuery / Snowflake)  
- Pipeline orchestration (Airflow)  
- Incremental data processing  
- Data quality validation  

---

## 👨‍💻 Author
Igor Matheus de França Fernandes

Data Engineering Portfolio Project
