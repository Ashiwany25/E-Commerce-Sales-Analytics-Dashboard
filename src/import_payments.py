
import pandas as pd
from sqlalchemy import create_engine, text
from getpass import getpass
from urllib.parse import quote_plus

# Load payment dataset
df = pd.read_csv(
    "data/raw/olist_order_payments_dataset.csv"
)

# Connect to MySQL
password = quote_plus(getpass("MySQL password: "))

engine = create_engine(
    f"mysql+pymysql://root:{password}"
    "@localhost:3306/ecommerce_analytics"
)

# Create and populate payments table
df.to_sql(
    "ecommerce_payments",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=1000
)

# Verify import
with engine.connect() as connection:
    result = connection.execute(
        text("SELECT COUNT(*) FROM ecommerce_payments")
    )
    print("Payment records imported:", result.scalar())

print("Payment data imported successfully!")
