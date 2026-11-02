# 🛒 E-Commerce Sales Analytics Dashboard

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://ashiwany-ecommerce-dashboard.streamlit.app/)
[![MySQL](https://img.shields.io/badge/MySQL-Analytics-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Plotly](https://img.shields.io/badge/Plotly-Visualizations-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Source_Code-181717?logo=github&logoColor=white)](https://github.com/Ashiwany25/E-Commerce-Sales-Analytics-Dashboard)

**🚀 [Live Dashboard](https://ashiwany-ecommerce-dashboard.streamlit.app/)** | **💻 [GitHub Repository](https://github.com/Ashiwany25/E-Commerce-Sales-Analytics-Dashboard)**

An interactive Business Intelligence dashboard built using **Python, Pandas, Plotly, Streamlit, and MySQL** to analyze sales performance, customer behavior, product categories, regional revenue, and delivery operations.

The project uses the **Brazilian E-Commerce Public Dataset by Olist**, featuring approximately 100,000 customer orders.

## 📊 Project Overview

The goal of this project is to transform raw e-commerce transactional data into meaningful business insights through data cleaning, SQL analysis, exploratory data analysis, and interactive visualizations.

The dashboard enables users to monitor key performance indicators, explore sales trends, identify top-performing categories, evaluate customer purchasing patterns, and analyze delivery performance.

## ✨ Key Features

- **Interactive Dashboard:** Five navigation tabs covering business performance, products, regions, customers, and operations.
- **Business KPIs:** Total revenue, total orders, unique customers, average order value, and items sold.
- **Sales Analysis:** Monthly revenue trends and top-performing product categories.
- **Regional Analytics:** Revenue and order distribution across Brazilian states.
- **Customer Analytics:** One-time versus repeat customers and purchase frequency.
- **Delivery Analytics:** Average delivery duration, on-time deliveries, and late delivery rate.
- **Payment Analytics:** Payment method distribution and payment values.
- **Dynamic Filters:** Filter results by date range, customer state, and product category.
- **Automated Business Insights:** Data-driven summaries that respond to dashboard filters.
- **CSV Export:** Download filtered sales data and analytics reports.
- **Data Quality Monitoring:** Missing values, duplicate records, and dataset information.
- **Automated Testing:** Pytest unit tests for key analytics calculations.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data analysis and application development |
| Pandas & NumPy | Data cleaning and transformation |
| Plotly | Interactive visualizations |
| Streamlit | Web dashboard |
| MySQL | Database storage and SQL analysis |
| Matplotlib & Seaborn | Exploratory data analysis |
| Pytest | Automated unit testing |
| Git & GitHub | Version control |

## 📂 Project Structure

```text
E-commerce Sales Analytics Dashboard/
├── .streamlit/
│   └── config.toml
├── app.py
├── assets/
├── deployment_data/
│   ├── cleaned_ecommerce_data.csv
│   └── olist_order_payments_dataset.csv
├── src/
│   ├── explore_data.py
│   ├── merge_data.py
│   ├── data_cleaning.py
│   ├── validate_data.py
│   ├── eda.py
│   ├── import_to_mysql.py
│   └── import_payments.py
├── sql/
│   └── SQL business analysis queries
├── tests/
│   └── test_analytics.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🏗️ Project Architecture

```text
Olist E-Commerce Dataset (9 CSV files)
                |
                v
        Data Exploration
      src/explore_data.py
                |
                v
        Data Integration
       src/merge_data.py
                |
                v
    Cleaning and Validation
  src/data_cleaning.py
  src/validate_data.py
                |
                v
      Processed Sales Data
                |
       +--------+--------+
       |                 |
       v                 v
   MySQL Database    Python Analytics
   SQL Queries       Pandas + Plotly
       |                 |
       +--------+--------+
                |
                v
      Streamlit Dashboard
             app.py
                |
                v
      Streamlit Cloud Deployment

Data Processing Workflow

1. Data Exploration: Inspect the source datasets, understand their structure, and identify missing values and data quality issues.

2. Data Integration: Merge related order, customer, product, and seller information into a consolidated analytical dataset.

3. Data Cleaning: Prepare delivered-order records, handle missing values, convert date columns, and calculate revenue and delivery metrics.

4. Data Validation: Check data consistency, duplicate records, and essential business metrics before analysis.

5. SQL Analysis: Load sales and payment information into MySQL and execute SQL queries to explore revenue, products, customers, and operations.

6. Exploratory Data Analysis: Use Pandas, Matplotlib, and Seaborn to investigate sales patterns and generate report visualizations.

7. Interactive Dashboard: Use Streamlit and Plotly to present filtered KPIs, sales trends, customer analytics, regional performance, and delivery insights.

8. Deployment and Testing: Run Pytest checks and deploy the dashboard on Streamlit Community Cloud using deployment-ready CSV files.

## 🗄️ SQL Business Analysis

MySQL was used to explore the consolidated sales and payment datasets and answer business questions through SQL queries.

### Business Questions

- How much revenue did the business generate?
- How did monthly revenue and order volume change over time?
- Which product categories generated the most revenue?
- Which Brazilian states contributed the most sales?
- How frequently did customers make repeat purchases?
- How did delivery performance compare with estimated delivery dates?
- Which payment methods were most commonly used?

### SQL Techniques

- `SELECT`, `WHERE`, `GROUP BY`, and `ORDER BY`
- Aggregate functions: `SUM()`, `COUNT()`, `AVG()`
- `JOIN` operations for combining relational tables
- Date-based aggregation for monthly trends
- Business KPI calculations

SQL scripts are available in the [`sql/` directory](sql/).

## 📌 Key Business Insights

The cleaned analytical dataset contains **110,197 order-item records**, representing **96,478 unique orders** and **93,358 unique customers**.

| Metric | Value |
|---|---:|
| Unique Orders | 96,478 |
| Unique Customers | 93,358 |
| Order-Item Records | 110,197 |
| Product Sales Revenue | R$13,221,498.11 |

**Interpretation:** These figures describe the cleaned, delivered-order dataset used for analysis. Product sales revenue excludes freight charges. The dashboard supports deeper investigation through date, state, and category filters.

**Important:** The analytical dataset is at order-item level, so order counts and customer counts must use distinct identifiers to avoid double-counting.
## 📈 Dashboard Sections

### 1. Sales Overview
Displays overall business KPIs and monthly revenue performance.

### 2. Product Analytics
Identifies the highest-revenue product categories.

### 3. Regional Sales
Compares revenue and order volume across Brazilian states.

### 4. Customer Analytics
Analyzes customer purchase frequency and repeat purchasing behavior.

### 5. Operations Analytics
Examines delivery performance and payment method trends.

## 📸 Dashboard Visualizations

Explore the interactive dashboard: **[Live Demo](https://ashiwany-ecommerce-dashboard.streamlit.app/)**

### 📈 Monthly Revenue Trend
![Monthly Revenue Trend](assets/monthly_revenue.png)

### 📊 Monthly Sales Growth
![Monthly Sales Growth](assets/monthly_sales_growth.png)

### 🛍️ Top 10 Product Categories
![Top 10 Product Categories](assets/top_10_categories.png)

### 🌎 State-wise Revenue
![State-wise Revenue](assets/state_wise_revenue.png)

### 👥 Customer Purchase Frequency
![Customer Purchase Frequency](assets/customer_purchase_frequency.png)

### 🚚 Delivery Performance
![Delivery Performance](assets/delivery_performance.png)

### 💳 Payment Methods
![Payment Methods](assets/payment_methods.png)

## 📊 Dataset

**Source:** [Brazilian E-Commerce Public Dataset by Olist — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

The dataset contains order, customer, product, payment, and delivery information from a Brazilian e-commerce marketplace.

**Data preparation:**
- Combined multiple relational CSV files.
- Filtered completed, delivered orders.
- Cleaned and validated key fields.
- Calculated revenue and delivery metrics.
- Prepared a consolidated dataset for dashboard analysis.

**Revenue definition:** Product sales value excluding freight charges.

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Ashiwany25/E-Commerce-Sales-Analytics-Dashboard.git
cd E-Commerce-Sales-Analytics-Dashboard
```

Replace the placeholders with your actual GitHub repository details after publishing.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
python -m streamlit run app.py
```

Open the local address shown in the terminal, usually `http://localhost:8501`.

The dashboard uses the included deployment-ready CSV files, so a running MySQL server is not required to view it.

## 🧪 Automated Testing

Run the unit tests using:

```bash
python -m pytest tests/test_analytics.py -v
```

The tests cover revenue calculations, order counts, customer metrics, regional sales, and product category aggregations.

## 💡 Business Value

This project demonstrates how e-commerce transaction data can support decisions involving revenue growth, product performance, customer retention, regional opportunities, and delivery efficiency.

## 🔮 Future Improvements

- Sales forecasting using machine learning
- Customer segmentation using RFM analysis
- Advanced cohort and retention analysis
- Automated data pipeline scheduling
- Additional profitability and seller performance metrics

## 📄 License

The Olist dataset is sourced from Kaggle. Dataset usage remains subject to the source's applicable terms. No separate software license has been specified for this repository.
