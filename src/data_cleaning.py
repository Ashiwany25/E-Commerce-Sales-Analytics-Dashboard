
import pandas as pd
from pathlib import Path

# 1. Define file paths
project_folder = Path(__file__).resolve().parent.parent

input_file = (
    project_folder / "data" / "processed"
    / "merged_ecommerce_data.csv"
)

output_file = (
    project_folder / "data" / "processed"
    / "cleaned_ecommerce_data.csv"
)

# 2. Load the merged dataset
df = pd.read_csv(input_file)

print("Original dataset shape:", df.shape)

# 3. Convert date columns
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "shipping_limit_date"
]

for col in date_columns:
    df[col] = pd.to_datetime(
        df[col], errors="coerce"
    )

# 4. Keep delivered orders
df = df[
    df["order_status"] == "delivered"
].copy()

print("After delivered filter:", df.shape)

# 5. Keep valid sales items
df = df[
    df["order_item_id"].notna()
    & df["product_id"].notna()
    & df["price"].notna()
    & (df["price"] >= 0)
    & df["order_purchase_timestamp"].notna()
].copy()

# 6. Remove duplicate order-item records
df = df.drop_duplicates(
    subset=["order_id", "order_item_id"]
)

# 7. Handle missing product categories
df["product_category_name"] = (
    df["product_category_name"].fillna("Unknown")
)

# 8. Calculate item revenue
df["revenue"] = df["price"]

# 9. Extract date features
df["order_date"] = df[
    "order_purchase_timestamp"
].dt.date

df["order_year"] = df[
    "order_purchase_timestamp"
].dt.year

df["order_month"] = df[
    "order_purchase_timestamp"
].dt.month

df["order_day"] = df[
    "order_purchase_timestamp"
].dt.day

# 10. Calculate delivery duration
df["delivery_days"] = (
    df["order_delivered_customer_date"]
    - df["order_purchase_timestamp"]
).dt.total_seconds() / 86400

# Treat negative durations as invalid
df.loc[
    df["delivery_days"] < 0,
    "delivery_days"
] = float("nan")

# 11. Save cleaned dataset
df.to_csv(output_file, index=False)

# 12. Print results
print("\nCleaning completed successfully!")
print("Final dataset shape:", df.shape)
print("Total unique orders:", df["order_id"].nunique())
print("Total unique customers:",
      df["customer_unique_id"].nunique())
print("Total revenue (BRL):",
      round(df["revenue"].sum(), 2))
print("Missing delivery durations:",
      df["delivery_days"].isna().sum())

print("\nSaved to:", output_file)
