import pandas as pd


def validate_data(data: pd.DataFrame) -> dict:
    issues = {}

    # 1. Missing values
    missing_values = data.isnull().sum()
    missing_values = missing_values[missing_values > 0]

    if not missing_values.empty:
        issues["missing_values"] = missing_values.to_dict()

    # 2. Duplicate order IDs
    duplicate_orders = data[data.duplicated("order_id", keep=False)]

    if not duplicate_orders.empty:
        issues["duplicate_orders"] = duplicate_orders[
            "order_id"
        ].unique().tolist()

    # 3. Negative quantities
    negative_quantity = data[data["quantity"] < 0]

    if not negative_quantity.empty:
        issues["negative_quantity"] = negative_quantity[
            "order_id"
        ].tolist()

    # 4. Negative prices
    negative_price = data[data["unit_price"] < 0]

    if not negative_price.empty:
        issues["negative_price"] = negative_price[
            "order_id"
        ].tolist()

    # 5. Invalid dates
    invalid_dates = pd.to_datetime(
        data["order_date"],
        errors="coerce"
    ).isna()

    if invalid_dates.any():
        issues["invalid_dates"] = data.loc[
            invalid_dates,
            "order_id"
        ].tolist()

    return issues

# testing if working
if __name__ == "__main__":
    from src.ingestion.csv_ingestion import load_csv

    data, metadata = load_csv(
        "data/raw/ecommerce_transactions.csv"
    )

    issues = validate_data(data)

    print("ARGUS DATA QUALITY REPORT")
    print("-------------------------")

    if not issues:
        print("No data quality issues detected.")
    else:
        for issue, records in issues.items():
            print(f"\n{issue}:")
            print(records)