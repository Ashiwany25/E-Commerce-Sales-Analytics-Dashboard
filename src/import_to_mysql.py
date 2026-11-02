
import pandas as pd
from pathlib import Path
from getpass import getpass
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# ===== IMPORT DATA INTO MYSQL =====

project_folder = Path(__file__).resolve().parent.parent

csv_file = (
    project_folder / "data" / "processed"
    / "cleaned_ecommerce_data.csv"
)

# Load cleaned dataset
df = pd.read_csv(csv_file)

print("Dataset loaded successfully!")
print("Total CSV rows:", len(df))

# Select columns matching the MySQL table
columns = [
    "order_id",
    "order_item_id",
    "customer_id",
    "customer_unique_id",
    "order_status",
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "customer_city",
    "customer_state",
    "product_id",
    "product_category_name",
    "seller_id",
    "price",
    "freight_value",
    "revenue",
    "order_year",
    "order_month",
    "order_day",
    "delivery_days"
]

df = df[columns].copy()

# Convert dates into datetime format
date_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# Convert missing numeric values to SQL NULL
# Pandas and SQLAlchemy handle NaN/NaT as NULL
# when inserting data.

# Get MySQL password
password = getpass("Enter MySQL root password: ")

# Create connection
connection_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password=password,
    host="localhost",
    port=3306,
    database="ecommerce_analytics"
)

engine = create_engine(connection_url)

# Check connection
with engine.connect() as connection:
    database_name = connection.execute(
        text("SELECT DATABASE()")
    ).scalar()

    print("Connected to:", database_name)

# Import records into existing table
with engine.begin() as connection:

    # Clear any previous imported records
    connection.execute(
        text("DELETE FROM ecommerce_sales")
    )

    # Insert cleaned dataset in batches
    df.to_sql(
        name="ecommerce_sales",
        con=connection,
        if_exists="append",
        index=False,
        chunksize=1000
    )

print("\nData imported successfully!")

# Verify imported rows
with engine.connect() as connection:
    total_rows = connection.execute(
        text("SELECT COUNT(*) FROM ecommerce_sales")
    ).scalar()

print("Total rows in MySQL:", total_rows)

if total_rows == len(df):
    print("CSV and MySQL row counts match!")
else:
    print("Warning: Row counts do not match!")
