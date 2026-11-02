import plotly.express as px
import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="E-Commerce Sales Analytics",
    page_icon="🛒",
    layout="wide"
)

# PROFESSIONAL DASHBOARD STYLING

st.markdown("""
<style>

/* Main dashboard spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

/* Main heading */
h1 {
    font-weight: 750;
    letter-spacing: -1px;
}

/* Section headings */
h2, h3 {
    font-weight: 650;
}

/* KPI cards */
div[data-testid="stMetric"] {
    background: #172033;
    border: 1px solid #29354A;
    border-radius: 14px;
    padding: 18px;
}

/* KPI labels */
div[data-testid="stMetricLabel"] {
    color: #94A3B8;
}

/* KPI values */
div[data-testid="stMetricValue"] {
    color: #F8FAFC;
    font-size: 1.65rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    border-right: 1px solid #29354A;
}

/* Chart containers */
div[data-testid="stPlotlyChart"] {
    border: 1px solid #29354A;
    border-radius: 14px;
    padding: 10px;
}

/* Horizontal dividers */
hr {
    border-color: #29354A;
}

</style>
""", unsafe_allow_html=True)


# Load cleaned dataset
@st.cache_data
def load_data():
    df = pd.read_csv(
        "deployment_data/cleaned_ecommerce_data.csv",
        parse_dates=["order_purchase_timestamp"]
    )
    return df


df = load_data()

# Sidebar
st.sidebar.title("🛒 E-Commerce Analytics")
st.sidebar.markdown("### Navigation")
st.sidebar.info(
    "Sales, customers, products, and delivery analytics."
)

# INTERACTIVE DASHBOARD FILTERS

st.sidebar.divider()
st.sidebar.header("Dashboard Filters")

# Date range filter
min_date = df["order_purchase_timestamp"].min().date()
max_date = df["order_purchase_timestamp"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# State filter
state_options = sorted(
    df["customer_state"].dropna().unique().tolist()
)

selected_states = st.sidebar.multiselect(
    "Select States",
    options=state_options,
    default=state_options
)

# Product category filter
category_options = sorted(
    df["product_category_name"]
    .dropna()
    .unique()
    .tolist()
)

selected_categories = st.sidebar.multiselect(
    "Select Product Categories",
    options=category_options,
    default=category_options
)

# Apply filters
filtered_df = df.copy()

if len(selected_dates) == 2:
    start_date, end_date = selected_dates

    filtered_df = filtered_df[
        filtered_df["order_purchase_timestamp"]
        .dt.date.between(start_date, end_date)
    ]

filtered_df = filtered_df[
    filtered_df["customer_state"].isin(selected_states)
]

filtered_df = filtered_df[
    filtered_df["product_category_name"].isin(
        selected_categories
    )
]

# Show active filtered row count
st.sidebar.caption(
    f"Matching sales records: {len(filtered_df):,}"
)

# All downstream analytics use the filtered data
df = filtered_df

if df.empty:
    st.warning(
        "No sales records match the selected filters. "
        "Please adjust your selections."
    )
    st.stop()


# Dashboard title
st.title("E-Commerce Sales Analytics")

st.caption(
    "Business Intelligence Dashboard | "
    "Revenue • Customers • Products • Delivery"
)

st.markdown(
    "Explore e-commerce performance through interactive "
    "KPIs, sales trends, customer insights, and regional analytics."
)

st.divider()

# Calculate KPIs
total_revenue = df["revenue"].sum()
total_orders = df["order_id"].nunique()
total_customers = df["customer_unique_id"].nunique()
total_items = len(df)
average_order_value = total_revenue / total_orders

# DASHBOARD NAVIGATION
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "📦 Products",
    "🌍 Regional Sales",
    "👥 Customers",
    "🚚 Operations"
])

with tab1:
    # KPI cards
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Total Revenue",
            f"R$ {total_revenue / 1_000_000:,.2f}M"
        )

    with col2:
        st.metric(
            "Total Orders",
            f"{total_orders:,}"
        )

    with col3:
        st.metric(
            "Total Customers",
            f"{total_customers:,}"
        )

    with col4:
        st.metric(
            "Average Order Value",
            f"R$ {average_order_value:,.2f}"
        )

    with col5:
        st.metric(
            "Items Sold",
            f"{total_items:,}"
        )

    st.divider()

    st.subheader("Sales Overview")


    # MONTHLY REVENUE ANALYSIS

    # Extract year and month
    df["sales_month"] = (
        df["order_purchase_timestamp"]
        .dt.to_period("M")
        .astype(str)
    )

    # Calculate monthly revenue
    monthly_revenue = (
        df.groupby("sales_month", as_index=False)["revenue"]
        .sum()
        .sort_values("sales_month")
    )

    # Create interactive line chart
    fig = px.line(
        monthly_revenue,
        x="sales_month",
        y="revenue",
        title="Monthly Revenue Trend",
        markers=True,
        labels={
            "sales_month": "Month",
            "revenue": "Revenue (R$)"
        }
    )

    fig.update_traces(
        line=dict(color="#3B82F6", width=3),
        marker=dict(size=7)
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Month",
        yaxis_title="Revenue (R$)",
        height=450
    )

    # Display chart
    st.plotly_chart(
        fig,
        use_container_width=True
    )

with tab2:
    # TOP 10 PRODUCT CATEGORIES

    st.divider()

    st.subheader("Top 10 Product Categories by Revenue")

    # Group sales by product category
    category_sales = (
        df.groupby("product_category_name", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .head(10)
    )

    # Sort for horizontal bar chart
    category_sales = category_sales.sort_values("revenue")

    # Create interactive bar chart
    fig_category = px.bar(
        category_sales,
        x="revenue",
        y="product_category_name",
        orientation="h",
        title="Best Performing Product Categories",
        labels={
            "revenue": "Total Revenue (R$)",
            "product_category_name": "Product Category"
        },
        color="revenue",
        color_continuous_scale="Blues"
    )

    fig_category.update_layout(
        height=500,
        showlegend=False,
        coloraxis_showscale=False,
        yaxis_title="",
        xaxis_title="Revenue (R$)"
    )

    # Display chart
    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

with tab3:
    # STATE-WISE REVENUE ANALYSIS

    st.divider()

    st.subheader("State-Wise Sales Analysis")

    # Calculate total revenue for each state
    state_sales = (
        df.groupby("customer_state", as_index=False)
        .agg(
            total_revenue=("revenue", "sum"),
            total_orders=("order_id", "nunique")
        )
        .sort_values("total_revenue", ascending=False)
    )

    # Create two columns
    col1, col2 = st.columns(2)

    # Chart 1: Revenue by state
    with col1:
        fig_state_revenue = px.bar(
            state_sales.head(10),
            x="customer_state",
            y="total_revenue",
            title="Top 10 States by Revenue",
            labels={
                "customer_state": "State",
                "total_revenue": "Revenue (R$)"
            },
            color="total_revenue",
            color_continuous_scale="Blues"
        )

        fig_state_revenue.update_layout(
            height=450,
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig_state_revenue,
            use_container_width=True
        )


    # Chart 2: Orders by state
    with col2:
        state_orders = state_sales.sort_values(
            "total_orders",
            ascending=False
        ).head(10)

        fig_state_orders = px.bar(
            state_orders,
            x="customer_state",
            y="total_orders",
            title="Top 10 States by Orders",
            labels={
                "customer_state": "State",
                "total_orders": "Total Orders"
            },
            color="total_orders",
            color_continuous_scale="Greens"
        )

        fig_state_orders.update_layout(
            height=450,
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig_state_orders,
            use_container_width=True
        )

with tab4:
    # CUSTOMER PURCHASE BEHAVIOR

    st.divider()

    st.subheader("Customer Purchase Behavior")

    # Count unique orders for each customer
    customer_orders = (
        df.groupby("customer_unique_id")["order_id"]
        .nunique()
        .reset_index(name="total_orders")
    )

    # Classify customers
    customer_orders["customer_type"] = (
        customer_orders["total_orders"].apply(
            lambda x: "Repeat Customer" if x > 1
            else "One-Time Customer"
        )
    )

    # Calculate customer metrics
    total_unique_customers = len(customer_orders)

    repeat_customers = (
        customer_orders["total_orders"] > 1
    ).sum()

    one_time_customers = (
        total_unique_customers - repeat_customers
    )

    repeat_rate = (
        repeat_customers / total_unique_customers * 100
        if total_unique_customers > 0 else 0
    )

    # Display KPI cards
    cust_col1, cust_col2, cust_col3 = st.columns(3)

    with cust_col1:
        st.metric(
            "One-Time Customers",
            f"{one_time_customers:,}"
        )

    with cust_col2:
        st.metric(
            "Repeat Customers",
            f"{repeat_customers:,}"
        )

    with cust_col3:
        st.metric(
            "Repeat Customer Rate",
            f"{repeat_rate:.2f}%"
        )

    # Customer type distribution
    customer_type_summary = (
        customer_orders["customer_type"]
        .value_counts()
        .reset_index()
    )

    customer_type_summary.columns = [
        "customer_type",
        "total_customers"
    ]

    # Purchase frequency distribution
    purchase_frequency = (
        customer_orders["total_orders"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    purchase_frequency.columns = [
        "number_of_orders",
        "number_of_customers"
    ]

    # Create two charts
    customer_chart1, customer_chart2 = st.columns(2)

    with customer_chart1:
        fig_customer_type = px.pie(
            customer_type_summary,
            names="customer_type",
            values="total_customers",
            title="One-Time vs Repeat Customers",
            hole=0.45
        )

        fig_customer_type.update_layout(height=450)

        st.plotly_chart(
            fig_customer_type,
            use_container_width=True
        )

    with customer_chart2:
        fig_purchase_frequency = px.bar(
            purchase_frequency,
            x="number_of_orders",
            y="number_of_customers",
            title="Customer Purchase Frequency",
            labels={
                "number_of_orders": "Number of Orders",
                "number_of_customers": "Number of Customers"
            },
            color="number_of_customers",
            color_continuous_scale="Blues"
        )

        fig_purchase_frequency.update_layout(
            height=450,
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig_purchase_frequency,
            use_container_width=True
        )

with tab5:
    # DELIVERY PERFORMANCE ANALYTICS

    st.divider()

    st.subheader("Delivery Performance Analytics")

    # One order can contain multiple products.
    # Keep only one record per order.
    delivery_df = df.drop_duplicates(
        subset=["order_id"]
    ).copy()

    # Convert delivery date columns
    delivery_df["order_delivered_customer_date"] = (
        pd.to_datetime(
            delivery_df["order_delivered_customer_date"],
            errors="coerce"
        )
    )

    delivery_df["order_estimated_delivery_date"] = (
        pd.to_datetime(
            delivery_df["order_estimated_delivery_date"],
            errors="coerce"
        )
    )

    # Calculate average delivery duration
    avg_delivery_days = delivery_df["delivery_days"].mean()

    # Keep orders with both delivery dates
    valid_deliveries = delivery_df.dropna(
        subset=[
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]
    ).copy()

    # Compare calendar dates
    valid_deliveries["is_late"] = (
        valid_deliveries[
            "order_delivered_customer_date"
        ].dt.normalize()
        >
        valid_deliveries[
            "order_estimated_delivery_date"
        ].dt.normalize()
    )

    # Calculate delivery metrics
    total_deliveries = len(valid_deliveries)

    late_deliveries = int(
        valid_deliveries["is_late"].sum()
    )

    on_time_deliveries = (
        total_deliveries - late_deliveries
    )

    late_percentage = (
        late_deliveries / total_deliveries * 100
        if total_deliveries > 0 else 0
    )

    # Display delivery KPI cards
    d1, d2, d3, d4 = st.columns(4)

    with d1:
        st.metric(
            "Avg Delivery Time",
            f"{avg_delivery_days:.1f} days"
        )

    with d2:
        st.metric(
            "Total Deliveries",
            f"{total_deliveries:,}"
        )

    with d3:
        st.metric(
            "On-Time Deliveries",
            f"{on_time_deliveries:,}"
        )

    with d4:
        st.metric(
            "Late Delivery Rate",
            f"{late_percentage:.2f}%"
        )

    # Average delivery time by state
    state_delivery = (
        delivery_df.groupby(
            "customer_state",
            as_index=False
        )
        .agg(
            avg_delivery_days=("delivery_days", "mean"),
            total_orders=("order_id", "nunique")
        )
        .sort_values(
            "avg_delivery_days",
            ascending=False
        )
    )

    # Create delivery performance chart
    fig_delivery = px.bar(
        state_delivery,
        x="customer_state",
        y="avg_delivery_days",
        title="Average Delivery Time by State",
        labels={
            "customer_state": "State",
            "avg_delivery_days": "Average Delivery Time (Days)"
        },
        color="avg_delivery_days",
        color_continuous_scale="Oranges"
    )

    fig_delivery.update_layout(
        height=450,
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_delivery,
        use_container_width=True
    )

    # PAYMENT METHOD ANALYTICS

    st.divider()

    st.subheader("Payment Method Analytics")

    # Load payment dataset
    @st.cache_data
    def load_payments():
        return pd.read_csv(
            "deployment_data/olist_order_payments_dataset.csv"
        )

    payments_df = load_payments()

    # Include only delivered orders from cleaned dataset
    delivered_order_ids = df["order_id"].unique()

    payments_df = payments_df[
        payments_df["order_id"].isin(delivered_order_ids)
    ].copy()

    # Calculate payment method summary
    payment_summary = (
        payments_df.groupby(
            "payment_type",
            as_index=False
        )
        .agg(
            total_orders=("order_id", "nunique"),
            payment_records=("order_id", "size"),
            total_payment_value=("payment_value", "sum")
        )
        .sort_values(
            "total_orders",
            ascending=False
        )
    )

    # Create two columns
    pay_col1, pay_col2 = st.columns(2)

    # Chart 1: Payment method distribution
    with pay_col1:
        fig_payment_pie = px.pie(
            payment_summary,
            names="payment_type",
            values="total_orders",
            title="Orders by Payment Method",
            hole=0.45
        )

        fig_payment_pie.update_traces(
            textposition="inside",
            textinfo="percent"
        )

        fig_payment_pie.update_layout(
            height=450
        )

        st.plotly_chart(
            fig_payment_pie,
            use_container_width=True
        )

    # Chart 2: Total payment value
    with pay_col2:
        fig_payment_value = px.bar(
            payment_summary,
            x="payment_type",
            y="total_payment_value",
            title="Payment Value by Method",
            labels={
                "payment_type": "Payment Method",
                "total_payment_value": "Payment Value (R$)"
            },
            color="payment_type"
        )

        fig_payment_value.update_layout(
            height=450,
            showlegend=False
        )

        st.plotly_chart(
            fig_payment_value,
            use_container_width=True
        )

    # Display payment summary table
    st.markdown("#### Payment Method Summary")

    st.dataframe(
        payment_summary,
        use_container_width=True,
        hide_index=True
    )

# DOWNLOAD ANALYTICS REPORTS

st.divider()
st.subheader("📥 Download Analytics Reports")

col1, col2, col3 = st.columns(3)

with col1:
    st.download_button(
        "Download Sales Data",
        df.to_csv(index=False).encode("utf-8"),
        "filtered_ecommerce_sales.csv",
        "text/csv",
        use_container_width=True
    )

with col2:
    st.download_button(
        "Download Monthly Revenue",
        monthly_revenue.to_csv(index=False).encode("utf-8"),
        "monthly_revenue_report.csv",
        "text/csv",
        use_container_width=True
    )

with col3:
    st.download_button(
        "Download Product Sales",
        category_sales.to_csv(index=False).encode("utf-8"),
        "product_category_sales.csv",
        "text/csv",
        use_container_width=True
    )


# AUTOMATED BUSINESS INSIGHTS

st.divider()
st.subheader("💡 Automated Business Insights")

# Best performing product category
top_category = (
    df.groupby("product_category_name")["revenue"]
    .sum()
    .idxmax()
)

# Highest revenue generating state
top_state = (
    df.groupby("customer_state")["revenue"]
    .sum()
    .idxmax()
)

# Highest revenue month
best_month = (
    monthly_revenue.loc[
        monthly_revenue["revenue"].idxmax(),
        "sales_month"
    ]
)

# Calculate repeat customer percentage
customer_order_counts = (
    df.groupby("customer_unique_id")["order_id"]
    .nunique()
)

repeat_customer_percentage = (
    (customer_order_counts > 1).mean() * 100
)

# Calculate on-time delivery percentage
on_time_percentage = (
    (valid_deliveries["is_late"] == False).mean() * 100
    if len(valid_deliveries) > 0 else 0
)

# Display insights
insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.info(
        f"🏆 **Top Product Category:** {top_category} "
        "generates the highest product revenue."
    )

    st.info(
        f"📍 **Top Revenue State:** {top_state} "
        "contributes the most to sales."
    )

    st.info(
        f"📈 **Best Sales Month:** {best_month} "
        "recorded the highest revenue."
    )

with insight_col2:
    st.info(
        f"👥 **Repeat Customer Rate:** "
        f"{repeat_customer_percentage:.2f}% of customers "
        "placed more than one order."
    )

    st.info(
        f"🚚 **On-Time Delivery Rate:** "
        f"{on_time_percentage:.2f}% of evaluated orders "
        "were delivered on or before their estimated date."
    )


# DATA QUALITY AND PROJECT INFORMATION

st.divider()
st.subheader("🔍 Data Quality & Project Information")

# Dataset quality metrics
total_records = len(df)
unique_orders = df["order_id"].nunique()
unique_customers = df["customer_unique_id"].nunique()

missing_revenue = int(df["revenue"].isna().sum())
missing_delivery_days = int(df["delivery_days"].isna().sum())

duplicate_order_items = (
    int(df.duplicated(subset=["order_id", "order_item_id"]).sum())
    if "order_item_id" in df.columns
    else int(df.duplicated().sum())
)

# Display data quality metrics
quality_col1, quality_col2, quality_col3 = st.columns(3)

with quality_col1:
    st.metric("Sales Records", f"{total_records:,}")
    st.metric("Unique Orders", f"{unique_orders:,}")

with quality_col2:
    st.metric("Unique Customers", f"{unique_customers:,}")
    st.metric("Missing Revenue Values", f"{missing_revenue:,}")

with quality_col3:
    st.metric("Missing Delivery Durations", f"{missing_delivery_days:,}")
    st.metric("Duplicate Order Items", f"{duplicate_order_items:,}")

# Dataset information
with st.expander("📁 About the Dataset"):
    st.markdown("""
    **Dataset:** Brazilian E-Commerce Public Dataset by Olist

    **Source:** Kaggle

    **Analysis includes:**
    - Sales and revenue trends
    - Product category performance
    - Regional sales distribution
    - Customer purchase behavior
    - Delivery performance
    - Payment method analytics

    **Revenue definition:** Product sales value, excluding freight.

    **Note:** Metrics reflect the currently selected dashboard filters.
    """)

# Technology information
with st.expander("🛠️ Technology Stack"):
    st.markdown("""
    - **Python:** Data processing and analytics
    - **Pandas:** Data cleaning and aggregation
    - **Plotly:** Interactive data visualizations
    - **Streamlit:** Dashboard application
    - **MySQL:** SQL-based business analysis
    - **VS Code:** Development environment
    - **Git & GitHub:** Version control and project hosting
    """)

st.caption(
    "E-Commerce Sales Analytics Dashboard | "
    "Built with Python, Pandas, Plotly, Streamlit & MySQL"
)
