import pandas as pd


def analyze_distributions(data: pd.DataFrame) -> dict:
    numerical_columns = [
        "quantity",
        "unit_price",
        "discount",
        "gross_amount",
        "discount_amount",
        "net_amount",
        "net_unit_price",
    ]

    results = {}

    for column in numerical_columns:
        series = data[column].dropna()

        results[column] = {
            "mean": round(series.mean(), 2),
            "median": round(series.median(), 2),
            "std": round(series.std(), 2),
            "min": round(series.min(), 2),
            "max": round(series.max(), 2),
            "skewness": round(series.skew(), 2),
        }

    return results


if __name__ == "__main__":
    from src.processing.data_loader import load_transactions_from_db
    from src.processing.transformer import transform_transactions
    from src.processing.feature_engineer import engineer_features

    data = load_transactions_from_db()

    transformed_data = transform_transactions(data)

    feature_data = engineer_features(transformed_data)

    results = analyze_distributions(feature_data)

    print("\n=== ARGUS DISTRIBUTION ANALYSIS ===")

    for column, stats in results.items():
        print(f"\n{column}")

        for metric, value in stats.items():
            print(f"  {metric}: {value}")