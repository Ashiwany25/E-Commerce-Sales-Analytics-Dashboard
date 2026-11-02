
import pandas as pd
from pathlib import Path

# Step 1: Locate the cleaned dataset
project_folder = Path(__file__).resolve().parent.parent

file_path = (
    project_folder / "data" / "processed"
    / "cleaned_ecommerce_data.csv"
)

# Step 2: Load the dataset
df = pd.read_csv(file_path)

print("===== E-COMMERCE SALES KPIs =====")

# Step 3: Calculate total revenue
total_revenue = df["revenue"].sum()

# Step 4: Calculate unique orders
total_orders = df["order_id"].nunique()

# Step 5: Calculate unique customers
total_customers = df["customer_unique_id"].nunique()

# Step 6: Calculate Average Order Value
average_order_value = total_revenue / total_orders

# Step 7: Calculate total products sold
total_products_sold = len(df)

# Step 8: Display KPIs
print(f"\nTotal Revenue: R$ {total_revenue:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Customers: {total_customers:,}")
print(f"Average Order Value: R$ {average_order_value:,.2f}")
print(f"Total Products Sold: {total_products_sold:,}")

print("\nKPI calculation completed successfully!")



# =====  MONTHLY SALES TREND =====

import matplotlib.pyplot as plt

# Convert order dates to datetime
df["order_purchase_timestamp"] = pd.to_datetime(
    df["order_purchase_timestamp"]
)

# Extract year and month
df["year_month"] = (
    df["order_purchase_timestamp"]
    .dt.to_period("M")
)

# Calculate monthly revenue
monthly_sales = (
    df.groupby("year_month")["revenue"]
    .sum()
    .sort_index()
)

print("\n===== MONTHLY SALES REPORT =====")
print(monthly_sales)

# Create the line chart
plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales.index.astype(str),
    monthly_sales.values,
    marker="o",
    linewidth=2
)

plt.title("Monthly E-Commerce Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue (BRL)")

plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save chart inside assets folder
chart_path = (
    project_folder / "assets"
    / "monthly_revenue.png"
)

plt.savefig(chart_path, dpi=300)

# Display chart
plt.show()

print("\nMonthly revenue chart saved successfully!")
print("Saved to:", chart_path)


# ===== TOP PRODUCT CATEGORIES =====

# Group products by category and calculate revenue
category_sales = (
    df.groupby("product_category_name")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

# Select the top 10 categories
top_10_categories = category_sales.head(10)

print("\n===== TOP 10 PRODUCT CATEGORIES =====")
print(top_10_categories)

# Create horizontal bar chart
plt.figure(figsize=(12, 7))

plt.barh(
    top_10_categories.index,
    top_10_categories.values,
    color="steelblue"
)

plt.title("Top 10 Product Categories by Revenue")
plt.xlabel("Total Revenue (BRL)")
plt.ylabel("Product Category")

# Highest revenue category at the top
plt.gca().invert_yaxis()

plt.grid(axis="x", alpha=0.3)
plt.tight_layout()

# Save chart
category_chart_path = (
    project_folder / "assets"
    / "top_10_categories.png"
)

plt.savefig(category_chart_path, dpi=300)

# Display chart
plt.show()

print("\nTop 10 category chart saved successfully!")
print("Saved to:", category_chart_path)


# ===== STATE-WISE SALES ANALYSIS =====

# Calculate revenue for each customer state
state_sales = (
    df.groupby("customer_state")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

# Select top 10 states
top_10_states = state_sales.head(10)

print("\n===== TOP 10 STATES BY REVENUE =====")
print(top_10_states)

# Calculate orders by state
state_orders = (
    df.groupby("customer_state")["order_id"]
    .nunique()
    .sort_values(ascending=False)
)

print("\n===== TOP 10 STATES BY ORDERS =====")
print(state_orders.head(10))

# Create horizontal bar chart
plt.figure(figsize=(12, 7))

plt.barh(
    top_10_states.index,
    top_10_states.values,
    color="teal"
)

plt.title("Top 10 Brazilian States by Revenue")
plt.xlabel("Total Revenue (BRL)")
plt.ylabel("Customer State")

# Highest revenue at the top
plt.gca().invert_yaxis()

plt.grid(axis="x", alpha=0.3)
plt.tight_layout()

# Save the chart
state_chart_path = (
    project_folder / "assets"
    / "state_wise_revenue.png"
)

plt.savefig(state_chart_path, dpi=300)

# Display chart
plt.show()

print("\nState-wise revenue chart saved successfully!")
print("Saved to:", state_chart_path)


# ===== DELIVERY PERFORMANCE ANALYSIS =====

# Convert delivery dates to datetime
df["order_delivered_customer_date"] = pd.to_datetime(
    df["order_delivered_customer_date"],
    errors="coerce"
)

df["order_estimated_delivery_date"] = pd.to_datetime(
    df["order_estimated_delivery_date"],
    errors="coerce"
)

# Use one row per order to avoid counting
# multi-item orders more than once
delivery_df = df.drop_duplicates(
    subset=["order_id"]
).copy()

# Calculate delivery statistics
average_delivery = delivery_df["delivery_days"].mean()
minimum_delivery = delivery_df["delivery_days"].min()
maximum_delivery = delivery_df["delivery_days"].max()

print("\n===== DELIVERY PERFORMANCE REPORT =====")

print(f"\nAverage Delivery Time: {average_delivery:.2f} days")
print(f"Fastest Delivery: {minimum_delivery:.2f} days")
print(f"Slowest Delivery: {maximum_delivery:.2f} days")

# Keep orders with both actual and estimated delivery dates
valid_deliveries = delivery_df.dropna(
    subset=[
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
).copy()

# Mark deliveries that arrived after the estimated date
valid_deliveries["is_late"] = (
    valid_deliveries["order_delivered_customer_date"].dt.normalize()
    > valid_deliveries["order_estimated_delivery_date"].dt.normalize()
)

late_orders = valid_deliveries["is_late"].sum()
total_deliveries = len(valid_deliveries)

late_percentage = (
    late_orders / total_deliveries * 100
    if total_deliveries > 0 else 0
)

print(f"\nLate Deliveries: {late_orders:,}")
print(f"Total Valid Deliveries: {total_deliveries:,}")
print(f"Late Delivery Percentage: {late_percentage:.2f}%")

# Average delivery time by customer state
state_delivery = (
    delivery_df.groupby("customer_state")["delivery_days"]
    .mean()
    .sort_values(ascending=False)
)

print("\n===== AVERAGE DELIVERY TIME BY STATE =====")
print(state_delivery)

# Plot the 10 states with the longest average delivery times
top_10_slowest_states = state_delivery.head(10)

plt.figure(figsize=(12, 7))

plt.barh(
    top_10_slowest_states.index,
    top_10_slowest_states.values,
    color="coral"
)

plt.title("Top 10 States with Longest Average Delivery Time")
plt.xlabel("Average Delivery Time (Days)")
plt.ylabel("Customer State")

plt.gca().invert_yaxis()
plt.grid(axis="x", alpha=0.3)
plt.tight_layout()

# Save chart
delivery_chart_path = (
    project_folder / "assets"
    / "delivery_performance.png"
)

plt.savefig(delivery_chart_path, dpi=300)

plt.show()

print("\nDelivery performance chart saved successfully!")
print("Saved to:", delivery_chart_path)


# ===== PAYMENT METHOD ANALYSIS =====

# Load the original payment dataset
payments_file = (
    project_folder / "data" / "raw"
    / "olist_order_payments_dataset.csv"
)

payments_df = pd.read_csv(payments_file)

print("\n===== PAYMENT METHOD ANALYSIS =====")

# Keep payments belonging to delivered orders
delivered_order_ids = df["order_id"].unique()

payments_df = payments_df[
    payments_df["order_id"].isin(delivered_order_ids)
].copy()

# One order may have multiple payment records.
# Count each order once per payment method.
payment_orders = (
    payments_df.groupby("payment_type")["order_id"]
    .nunique()
    .sort_values(ascending=False)
)

print("\nOrders by Payment Method:")
print(payment_orders)

# Calculate percentage of delivered orders
total_delivered_orders = df["order_id"].nunique()

payment_percentage = (
    payment_orders / total_delivered_orders * 100
)

print("\nPercentage of Orders by Payment Method:")
print(payment_percentage.round(2))

# Calculate total payment value by method
payment_values = (
    payments_df.groupby("payment_type")["payment_value"]
    .sum()
    .sort_values(ascending=False)
)

print("\nPayment Value by Method (BRL):")
print(payment_values.round(2))

# Create bar chart
plt.figure(figsize=(10, 6))

plt.bar(
    payment_orders.index,
    payment_orders.values,
    color="mediumseagreen"
)

plt.title("Payment Methods Used for Delivered Orders")
plt.xlabel("Payment Method")
plt.ylabel("Number of Unique Orders")

plt.xticks(rotation=30)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

# Save chart
payment_chart_path = (
    project_folder / "assets"
    / "payment_methods.png"
)

plt.savefig(payment_chart_path, dpi=300)

plt.show()

print("\nPayment method chart saved successfully!")
print("Saved to:", payment_chart_path)


# ===== CUSTOMER PURCHASE BEHAVIOR =====

# Keep one row per order to avoid counting
# multiple products as separate purchases
customer_orders = df[
    ["customer_unique_id", "order_id"]
].drop_duplicates()

# Count orders placed by each unique customer
purchase_frequency = (
    customer_orders.groupby("customer_unique_id")["order_id"]
    .nunique()
)

# Calculate customer metrics
total_unique_customers = len(purchase_frequency)

one_time_customers = (
    purchase_frequency == 1
).sum()

repeat_customers = (
    purchase_frequency > 1
).sum()

repeat_customer_percentage = (
    repeat_customers / total_unique_customers * 100
    if total_unique_customers > 0 else 0
)

print("\n===== CUSTOMER PURCHASE BEHAVIOR =====")

print(f"\nTotal Unique Customers: {total_unique_customers:,}")
print(f"One-Time Customers: {one_time_customers:,}")
print(f"Repeat Customers: {repeat_customers:,}")
print(f"Repeat Customer Percentage: {repeat_customer_percentage:.2f}%")

# Group customers by purchase frequency
purchase_distribution = (
    purchase_frequency.value_counts()
    .sort_index()
)

print("\n===== PURCHASE FREQUENCY DISTRIBUTION =====")
print(purchase_distribution)

# Create a chart showing customers with
# 1, 2, 3, 4, and 5+ purchases
purchase_groups = pd.cut(
    purchase_frequency,
    bins=[0, 1, 2, 3, 4, float("inf")],
    labels=["1", "2", "3", "4", "5+"]
)

purchase_group_counts = (
    purchase_groups.value_counts()
    .reindex(["1", "2", "3", "4", "5+"], fill_value=0)
)

plt.figure(figsize=(10, 6))

plt.bar(
    purchase_group_counts.index,
    purchase_group_counts.values,
    color="mediumpurple"
)

plt.title("Customer Purchase Frequency")
plt.xlabel("Number of Purchases")
plt.ylabel("Number of Customers")

plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

# Save chart
customer_chart_path = (
    project_folder / "assets"
    / "customer_purchase_frequency.png"
)

plt.savefig(customer_chart_path, dpi=300)

plt.show()

print("\nCustomer purchase frequency chart saved!")
print("Saved to:", customer_chart_path)


# ===== MONTH-OVER-MONTH SALES GROWTH =====

# Calculate monthly revenue from the cleaned dataset
monthly_growth_df = (
    df.groupby("year_month")["revenue"]
    .sum()
    .sort_index()
    .to_frame(name="revenue")
)

# Calculate percentage change from previous month
monthly_growth_df["mom_growth_pct"] = (
    monthly_growth_df["revenue"].pct_change(
        fill_method=None
    ) * 100
)

# First month has no previous month for comparison
print("\n===== MONTHLY SALES GROWTH REPORT =====")
print(monthly_growth_df.round(2))

# Calculate highest and lowest growth months
valid_growth = monthly_growth_df[
    "mom_growth_pct"
].dropna()

if not valid_growth.empty:
    highest_growth_month = valid_growth.idxmax()
    lowest_growth_month = valid_growth.idxmin()

    print("\nHighest Growth Month:", highest_growth_month)
    print(
        "Highest Growth:",
        f"{valid_growth.max():.2f}%"
    )

    print("\nLowest Growth Month:", lowest_growth_month)
    print(
        "Lowest Growth:",
        f"{valid_growth.min():.2f}%"
    )

# Create line chart
plt.figure(figsize=(12, 6))

plt.plot(
    monthly_growth_df.index.astype(str),
    monthly_growth_df["mom_growth_pct"],
    marker="o",
    linewidth=2,
    color="royalblue"
)

# Zero line separates positive and negative growth
plt.axhline(
    y=0,
    color="red",
    linestyle="--",
    linewidth=1
)

plt.title("Month-over-Month Revenue Growth")
plt.xlabel("Month")
plt.ylabel("Revenue Growth (%)")

plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save chart
growth_chart_path = (
    project_folder / "assets"
    / "monthly_sales_growth.png"
)

plt.savefig(growth_chart_path, dpi=300)

plt.show()

print("\nMonthly sales growth chart saved successfully!")
print("Saved to:", growth_chart_path)


# ===== EXPORT EDA SUMMARY REPORTS =====

# Create reports folder if it does not exist
reports_folder = project_folder / "data" / "reports"
reports_folder.mkdir(parents=True, exist_ok=True)

# 1. Export monthly revenue
monthly_sales.rename("revenue").to_csv(
    reports_folder / "monthly_revenue.csv",
    header=True
)

# 2. Export category-wise revenue
category_sales.rename("revenue").to_csv(
    reports_folder / "category_sales.csv",
    header=True
)

# 3. Export state-wise revenue
state_sales.rename("revenue").to_csv(
    reports_folder / "state_sales.csv",
    header=True
)

# 4. Export state-wise order counts
state_orders.rename("total_orders").to_csv(
    reports_folder / "state_orders.csv",
    header=True
)

# 5. Export delivery performance by state
state_delivery.rename("average_delivery_days").to_csv(
    reports_folder / "state_delivery.csv",
    header=True
)

# 6. Export payment method analysis
payment_summary = pd.DataFrame({
    "total_orders": payment_orders,
    "order_percentage": payment_percentage,
    "total_payment_value": payment_values
})

payment_summary.to_csv(
    reports_folder / "payment_summary.csv",
    index_label="payment_type"
)

# 7. Export customer purchase frequency
purchase_group_counts.rename(
    "total_customers"
).to_csv(
    reports_folder / "customer_purchase_frequency.csv",
    header=True,
    index_label="number_of_purchases"
)

# 8. Export monthly revenue growth
monthly_growth_df.to_csv(
    reports_folder / "monthly_growth.csv"
)

# 9. Export overall business KPIs
kpi_summary = pd.DataFrame([{
    "total_revenue": total_revenue,
    "total_orders": total_orders,
    "total_customers": total_customers,
    "average_order_value": average_order_value,
    "total_products_sold": total_products_sold,
    "repeat_customers": repeat_customers,
    "repeat_customer_percentage": repeat_customer_percentage,
    "average_delivery_days": average_delivery,
    "late_delivery_percentage": late_percentage
}])

kpi_summary.to_csv(
    reports_folder / "kpi_summary.csv",
    index=False
)

print("\n===== EDA REPORT EXPORT =====")
print("All EDA reports exported successfully!")

for file in sorted(reports_folder.glob("*.csv")):
    print(file.name)
