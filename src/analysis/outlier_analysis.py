import pandas as pd


def detect_outliers(
    data: pd.DataFrame,
    column: str
) -> pd.DataFrame:

    series = data[column].dropna()

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)

    outliers = data[
        (data[column] < lower_bound)
        | (data[column] > upper_bound)
    ].copy()

    return outliers


if __name__ == "__main__":
    from src.processing.data_loader import load_transactions_from_db
    from src.processing.transformer import transform_transactions
    from src.processing.feature_engineer import engineer_features

    data = load_transactions_from_db()

    transformed_data = transform_transactions(data)

    feature_data = engineer_features(transformed_data)

    column = "net_amount"

    outliers = detect_outliers(
        feature_data,
        column
    )

    print("\n=== ARGUS OUTLIER ANALYSIS ===")
    print(f"Column: {column}")
    print(f"Total records: {len(feature_data)}")
    print(f"Outliers detected: {len(outliers)}")

    if len(outliers) > 0:
        print("\nOutlier records:")
        print(
            outliers[
                [
                    "order_id",
                    "customer_id",
                    "product_id",
                    "net_amount"
                ]
            ]
        )
    else:
        print("\nNo outliers detected.")