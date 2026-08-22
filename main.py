from datetime import datetime

from src.ingestion.csv_ingestion import load_csv
from src.processing.validator import validate_data
from src.processing.data_processor import separate_data
from src.processing.database_loader import (
    load_transactions,
    log_ingestion,
)


DATA_PATH = "data/raw/ecommerce_transactions.csv"


def main():
    print("================================")
    print("          ARGUS STARTING")
    print("================================")

    # 1. Ingestion
    data, metadata = load_csv(DATA_PATH)

    print(f"\nRows received: {metadata['rows']}")
    print(f"Columns received: {metadata['columns']}")

    # 2. Validation
    validated_data, report = validate_data(data)

    print("\nData quality:")
    print(f"Valid records: {report['valid_records']}")
    print(f"Invalid records: {report['invalid_records']}")
    print(f"Quality score: {report['quality_score']}%")

    # 3. Separate valid and invalid data
    valid_data, invalid_data = separate_data(validated_data)

    # 4. Load valid records into PostgreSQL
    inserted = load_transactions(valid_data)

    print(f"\nInserted {inserted} transactions into PostgreSQL.")

    # 5. Log ingestion
    log_ingestion(
        source=metadata["source"],
        ingested_at=datetime.now().isoformat(),
        rows_received=report["total_records"],
        columns_received=metadata["columns"],
        valid_records=report["valid_records"],
        invalid_records=report["invalid_records"],
        quality_score=report["quality_score"],
    )

    print("Ingestion logged successfully.")
    print("\n================================")
    print("          ARGUS COMPLETE")
    print("================================")


if __name__ == "__main__":
    main()