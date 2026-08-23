import pandas as pd


def transform_transactions(data: pd.DataFrame) -> pd.DataFrame:
    transformed = data.copy()

    transformed["gross_amount"] = (
        transformed["quantity"] * transformed["unit_price"]
    )

    transformed["discount_amount"] = (
        transformed["gross_amount"] * transformed["discount"]
    )

    transformed["net_amount"] = (
        transformed["gross_amount"]
        - transformed["discount_amount"]
    )

    return transformed


if __name__ == "__main__":
    from src.processing.data_loader import load_transactions_from_db

    data = load_transactions_from_db()

    transformed_data = transform_transactions(data)

    print("=== TRANSFORMED DATA ===")
    print(transformed_data.head())

    print("\n=== NEW FEATURES ===")
    print(
        transformed_data[
            [
                "gross_amount",
                "discount_amount",
                "net_amount"
            ]
        ].head()
    )