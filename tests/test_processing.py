import pandas as pd

from src.processing.transformer import transform_transactions
from src.processing.feature_engineer import engineer_features
from src.processing.feature_validator import validate_features


def create_test_data():
    return pd.DataFrame({
        "order_id": [1, 2],
        "customer_id": [101, 102],
        "product_id": [201, 202],
        "order_date": ["2026-08-01", "2026-08-02"],
        "quantity": [2, 3],
        "unit_price": [500.0, 1000.0],
        "discount": [0.10, 0.20],
        "region": ["North", "South"],
        "payment_method": ["UPI", "Card"],
    })


def test_transformation():
    data = create_test_data()

    result = transform_transactions(data)

    assert "gross_amount" in result.columns
    assert "discount_amount" in result.columns
    assert "net_amount" in result.columns

    assert result.loc[0, "gross_amount"] == 1000
    assert result.loc[0, "discount_amount"] == 100
    assert result.loc[0, "net_amount"] == 900


def test_feature_engineering():
    data = create_test_data()

    transformed = transform_transactions(data)
    result = engineer_features(transformed)

    expected_features = [
        "net_unit_price",
        "transaction_size",
        "order_year",
        "order_month",
        "order_day",
    ]

    for feature in expected_features:
        assert feature in result.columns


def test_feature_validation():
    data = create_test_data()

    transformed = transform_transactions(data)
    features = engineer_features(transformed)

    report = validate_features(features)

    assert report["is_valid"] is True