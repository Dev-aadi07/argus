import pandas as pd


def validate_features(data: pd.DataFrame) -> dict:
    report = {}

    required_features = [
        "gross_amount",
        "discount_amount",
        "net_amount",
        "net_unit_price",
        "transaction_size",
        "order_year",
        "order_month",
        "order_day",
    ]

    # Check required columns
    missing_features = [
        column
        for column in required_features
        if column not in data.columns
    ]

    report["missing_features"] = missing_features

    # Check missing values
    report["missing_values"] = (
        data[required_features]
        .isnull()
        .sum()
        .to_dict()
    )

    # Check negative monetary values
    report["negative_net_amount"] = int(
        (data["net_amount"] < 0).sum()
    )

    report["negative_gross_amount"] = int(
        (data["gross_amount"] < 0).sum()
    )

    # Check invalid transaction categories
    valid_sizes = {"small", "medium", "large"}

    actual_sizes = set(
        data["transaction_size"]
        .dropna()
        .astype(str)
        .unique()
    )

    report["invalid_transaction_sizes"] = sorted(
        actual_sizes - valid_sizes
    )

    # Overall validity
    report["is_valid"] = (
        len(missing_features) == 0
        and all(
            value == 0
            for value in report["missing_values"].values()
        )
        and report["negative_net_amount"] == 0
        and report["negative_gross_amount"] == 0
        and len(report["invalid_transaction_sizes"]) == 0
    )

    return report


if __name__ == "__main__":
    from src.processing.data_loader import load_transactions_from_db
    from src.processing.transformer import transform_transactions
    from src.processing.feature_engineer import engineer_features

    data = load_transactions_from_db()

    transformed_data = transform_transactions(data)

    feature_data = engineer_features(transformed_data)

    report = validate_features(feature_data)

    print("=== FEATURE VALIDATION REPORT ===")

    for key, value in report.items():
        print(f"{key}: {value}")