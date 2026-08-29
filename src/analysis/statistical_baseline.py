import pandas as pd


def generate_baseline(data: pd.DataFrame) -> dict:
    columns = [
        "quantity",
        "unit_price",
        "discount",
        "gross_amount",
        "discount_amount",
        "net_amount",
        "net_unit_price",
    ]

    baseline = {}

    for column in columns:
        series = data[column].dropna()

        baseline[column] = {
            "mean": round(series.mean(), 2),
            "median": round(series.median(), 2),
            "std": round(series.std(), 2),
            "q1": round(series.quantile(0.25), 2),
            "q3": round(series.quantile(0.75), 2),
            "min": round(series.min(), 2),
            "max": round(series.max(), 2),
        }

    return baseline


if __name__ == "__main__":
    from src.processing.data_loader import load_transactions_from_db
    from src.processing.transformer import transform_transactions
    from src.processing.feature_engineer import engineer_features

    data = load_transactions_from_db()

    transformed_data = transform_transactions(data)

    feature_data = engineer_features(transformed_data)

    baseline = generate_baseline(feature_data)

    print("\n=== ARGUS STATISTICAL BASELINE ===")

    for column, stats in baseline.items():

        print(f"\n{column}")

        for metric, value in stats.items():
            print(f"  {metric}: {value}")