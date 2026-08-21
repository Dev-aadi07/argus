from src.ingestion.csv_ingestion import load_csv
from src.processing.validator import validate_data
from src.processing.data_processor import (
    separate_data,
    save_processed_data,
)


def main():

    print("================================")
    print("          ARGUS STARTING")
    print("================================")

    # -------------------------
    # 1. INGESTION
    # -------------------------

    data, metadata = load_csv(
        "data/raw/ecommerce_transactions.csv"
    )

    print("\n[1] DATA INGESTION")
    print(f"Records received: {metadata['rows']}")
    print(f"Columns received: {metadata['columns']}")

    # -------------------------
    # 2. VALIDATION
    # -------------------------

    validated_data, report = validate_data(data)

    print("\n[2] DATA VALIDATION")
    print(f"Valid records: {report['valid_records']}")
    print(f"Invalid records: {report['invalid_records']}")
    print(f"Quality score: {report['quality_score']}%")

    # -------------------------
    # 3. SEPARATION
    # -------------------------

    valid_data, invalid_data = separate_data(
        validated_data
    )

    print("\n[3] DATA SEPARATION")
    print(f"Processed records: {len(valid_data)}")
    print(f"Quarantined records: {len(invalid_data)}")

    # -------------------------
    # 4. SAVE
    # -------------------------

    processed_path, quarantine_path = save_processed_data(
        valid_data,
        invalid_data
    )

    print("\n[4] OUTPUT")
    print(f"Processed data: {processed_path}")
    print(f"Quarantined data: {quarantine_path}")

    print("\n================================")
    print("       ARGUS PIPELINE DONE")
    print("================================")


if __name__ == "__main__":
    main()