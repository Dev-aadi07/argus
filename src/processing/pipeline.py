from src.processing.data_loader import load_transactions_from_db
from src.processing.transformer import transform_transactions
from src.processing.feature_engineer import engineer_features
from src.processing.feature_validator import validate_features
from src.processing.data_writer import save_processed_data


def run_processing_pipeline():
    print("\n=== ARGUS PROCESSING PIPELINE ===")

    # 1. Load data from PostgreSQL
    data = load_transactions_from_db()
    print(f"Loaded {len(data)} transactions.")

    # 2. Transform data
    transformed_data = transform_transactions(data)
    print("Transformation completed.")

    # 3. Engineer features
    feature_data = engineer_features(transformed_data)
    print("Feature engineering completed.")

    # 4. Validate features
    report = validate_features(feature_data)

    print("\nFeature validation:")
    print(f"Valid: {report['is_valid']}")

    if not report["is_valid"]:
        print("Feature validation failed.")
        print(report)
        raise ValueError(
            "Processing pipeline stopped because "
            "feature validation failed."
        )

    # 5. Save processed dataset
    save_processed_data(feature_data)

    print("\n=== PROCESSING COMPLETE ===")

    return feature_data


if __name__ == "__main__":
    run_processing_pipeline()