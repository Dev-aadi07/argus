import pandas as pd


def calculate_correlations(data: pd.DataFrame) -> pd.DataFrame:
    numerical_columns = [
        "quantity",
        "unit_price",
        "discount",
        "gross_amount",
        "discount_amount",
        "net_amount",
        "net_unit_price",
    ]

    return data[numerical_columns].corr()


if __name__ == "__main__":
    from src.processing.data_loader import load_transactions_from_db
    from src.processing.transformer import transform_transactions
    from src.processing.feature_engineer import engineer_features

    data = load_transactions_from_db()

    transformed_data = transform_transactions(data)

    feature_data = engineer_features(transformed_data)

    correlation_matrix = calculate_correlations(feature_data)

    print("\n=== ARGUS CORRELATION MATRIX ===")
    print(correlation_matrix.round(2))