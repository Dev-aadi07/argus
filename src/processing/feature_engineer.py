import pandas as pd


def engineer_features(data: pd.DataFrame) -> pd.DataFrame:
    features = data.copy()

    # Average value of each unit after discount
    features["net_unit_price"] = (
        features["net_amount"] / features["quantity"]
    )

    # Categorize transaction size
    features["transaction_size"] = pd.cut(
        features["net_amount"],
        bins=[-1, 500, 1500, float("inf")],
        labels=["small", "medium", "large"]
    )
    
    
    # Ensure order_date is datetime
    features["order_date"] = pd.to_datetime(
        features["order_date"],
        errors="coerce"
    )

    # Extract useful date features
    features["order_year"] = features["order_date"].dt.year
    features["order_month"] = features["order_date"].dt.month
    features["order_day"] = features["order_date"].dt.day

    return features


if __name__ == "__main__":
    from src.processing.data_loader import load_transactions_from_db
    from src.processing.transformer import transform_transactions

    data = load_transactions_from_db()

    transformed_data = transform_transactions(data)

    feature_data = engineer_features(transformed_data)

    print("=== FEATURE ENGINEERED DATA ===")
    print(feature_data.head())

    print("\n=== NEW FEATURES ===")
    print(
        feature_data[
            [
                "net_unit_price",
                "transaction_size",
                "order_year",
                "order_month",
                "order_day"
            ]
        ].head()
    )