import pandas as pd


def validate_data(data: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    validation = pd.DataFrame(index=data.index)

    # Check 1: Missing unit price
    validation["missing_unit_price"] = data["unit_price"].isnull()

    # Check 2: Duplicate order ID
    validation["duplicate_order"] = data.duplicated(
        "order_id",
        keep=False
    )

    # Check 3: Negative quantity
    validation["negative_quantity"] = data["quantity"] < 0

    # Check 4: Negative price
    validation["negative_price"] = data["unit_price"] < 0

    # Check 5: Invalid date
    validation["invalid_date"] = pd.to_datetime(
        data["order_date"],
        errors="coerce"
    ).isna()

    # Combine all validation failures
    validation["is_invalid"] = validation.any(axis=1)

    # Build reasons for each invalid row
    validation["issues"] = validation.apply(
        get_issues,
        axis=1
    )

    # Add validation information to a copy of the data
    result = data.copy()

    result["is_valid"] = ~validation["is_invalid"]
    result["issues"] = validation["issues"]

    # Summary
    total_records = len(result)
    invalid_records = validation["is_invalid"].sum()
    valid_records = total_records - invalid_records

    quality_score = (
        valid_records / total_records * 100
        if total_records > 0
        else 0
    )

    report = {
        "total_records": total_records,
        "valid_records": valid_records,
        "invalid_records": invalid_records,
        "quality_score": round(quality_score, 2),
    }

    return result, report


def get_issues(row) -> str:
    issues = []

    if row["missing_unit_price"]:
        issues.append("missing_unit_price")

    if row["duplicate_order"]:
        issues.append("duplicate_order")

    if row["negative_quantity"]:
        issues.append("negative_quantity")

    if row["negative_price"]:
        issues.append("negative_price")

    if row["invalid_date"]:
        issues.append("invalid_date")

    return ", ".join(issues)
  
  
  
if __name__ == "__main__":
    from src.ingestion.csv_ingestion import load_csv

    data, metadata = load_csv(
        "data/raw/ecommerce_transactions.csv"
    )

    validated_data, report = validate_data(data)

    print("ARGUS DATA QUALITY REPORT")
    print("=========================")

    print(f"Total records:  {report['total_records']}")
    print(f"Valid records:  {report['valid_records']}")
    print(f"Invalid records: {report['invalid_records']}")
    print(f"Quality score:  {report['quality_score']}%")

    print("\nInvalid records:")
    print("----------------")

    invalid_data = validated_data[
        ~validated_data["is_valid"]
    ]

    print(
        invalid_data[
            ["order_id", "is_valid", "issues"]
        ].to_string(index=False)
    )