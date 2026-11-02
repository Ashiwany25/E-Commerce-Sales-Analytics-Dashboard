
import pandas as pd
from pathlib import Path

# Locate cleaned dataset
project_folder = Path(__file__).resolve().parent.parent

file_path = (
    project_folder / "data" / "processed"
    / "cleaned_ecommerce_data.csv"
)

# Load cleaned data
df = pd.read_csv(file_path)

print("===== DATA VALIDATION REPORT =====")

# Check dataset dimensions
print("\nTotal rows:", df.shape[0])
print("Total columns:", df.shape[1])

# Check missing prices
print("\nMissing prices:", df["price"].isna().sum())

# Check duplicate order-item keys
duplicates = df.duplicated(
    subset=["order_id", "order_item_id"]
).sum()

print("Duplicate order items:", duplicates)

# Check order statuses
print("\nOrder statuses:")
print(df["order_status"].value_counts())

# Check invalid revenue
print("\nNegative revenue records:",
      (df["revenue"] < 0).sum())

# Check unique orders
print("\nUnique orders:", df["order_id"].nunique())

# Check total revenue
print("Total revenue (BRL):",
      round(df["revenue"].sum(), 2))

# Validate important conditions
assert df["price"].notna().all()
assert (df["price"] >= 0).all()
assert (df["order_status"] == "delivered").all()
assert duplicates == 0

print("\nAll data validation checks passed!")
