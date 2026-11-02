
import pandas as pd
from pathlib import Path

# Locate project folders
project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data" / "raw"

# Load four datasets
orders = pd.read_csv(data_folder / "olist_orders_dataset.csv")
customers = pd.read_csv(data_folder / "olist_customers_dataset.csv")
items = pd.read_csv(data_folder / "olist_order_items_dataset.csv")
products = pd.read_csv(data_folder / "olist_products_dataset.csv")

# Merge orders with customers
merged_data = pd.merge(
    orders,
    customers,
    on="customer_id",
    how="left",
    validate="many_to_one"
)

# Merge order items
merged_data = pd.merge(
    merged_data,
    items,
    on="order_id",
    how="left",
    validate="one_to_many"
)

# Merge product information
merged_data = pd.merge(
    merged_data,
    products,
    on="product_id",
    how="left",
    validate="many_to_one"
)

# Display results
print("Merged dataset shape:", merged_data.shape)

print("\nFirst 5 rows:")
print(merged_data.head())

print("\nTotal unique orders:")
print(merged_data["order_id"].nunique())

print("\nTotal unique products:")
print(merged_data["product_id"].nunique())

print("\nTotal item sales revenue (BRL):")
print(round(merged_data["price"].sum(), 2))

# Save merged dataset
output_folder = project_folder / "data" / "processed"
output_folder.mkdir(parents=True, exist_ok=True)

merged_data.to_csv(
    output_folder / "merged_ecommerce_data.csv",
    index=False
)

print("\nMerged dataset saved successfully!")
