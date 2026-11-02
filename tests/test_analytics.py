
import pandas as pd
import pytest


# Sample data for testing
@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "order_id": ["O1", "O1", "O2", "O3"],
        "customer_unique_id": ["C1", "C1", "C1", "C2"],
        "revenue": [100, 200, 150, 250],
        "customer_state": ["SP", "SP", "RJ", "RJ"],
        "product_category_name": [
            "Electronics", "Electronics",
            "Fashion", "Fashion"
        ]
    })


# Test 1: Total revenue
def test_total_revenue(sample_data):
    total_revenue = sample_data["revenue"].sum()
    assert total_revenue == 700


# Test 2: Unique orders
def test_unique_orders(sample_data):
    total_orders = sample_data["order_id"].nunique()
    assert total_orders == 3


# Test 3: Unique customers
def test_unique_customers(sample_data):
    total_customers = (
        sample_data["customer_unique_id"].nunique()
    )
    assert total_customers == 2


# Test 4: Average order value
def test_average_order_value(sample_data):
    revenue = sample_data["revenue"].sum()
    orders = sample_data["order_id"].nunique()

    average_order_value = revenue / orders

    assert average_order_value == pytest.approx(233.33, abs=0.01)


# Test 5: Repeat customer rate
def test_repeat_customer_rate(sample_data):
    customer_orders = (
        sample_data.groupby("customer_unique_id")["order_id"]
        .nunique()
    )

    repeat_rate = (customer_orders > 1).mean() * 100

    assert repeat_rate == 50.0


# Test 6: Missing revenue values
def test_missing_revenue(sample_data):
    missing_values = sample_data["revenue"].isna().sum()
    assert missing_values == 0


# Test 7: Revenue by state
def test_state_revenue(sample_data):
    state_revenue = (
        sample_data.groupby("customer_state")["revenue"]
        .sum()
    )

    assert state_revenue["SP"] == 300
    assert state_revenue["RJ"] == 400


# Test 8: Revenue by category
def test_category_revenue(sample_data):
    category_revenue = (
        sample_data.groupby("product_category_name")["revenue"]
        .sum()
    )

    assert category_revenue["Electronics"] == 300
    assert category_revenue["Fashion"] == 400
