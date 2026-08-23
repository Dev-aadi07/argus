from pathlib import Path

import pandas as pd


PROCESSED_PATH = Path("data/processed/transactions_features.csv")


def save_processed_data(data: pd.DataFrame) -> None:
    PROCESSED_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    data.to_csv(
        PROCESSED_PATH,
        index=False
    )

    print(
        f"Saved {len(data)} processed records to "
        f"{PROCESSED_PATH}"
    )


if __name__ == "__main__":
    from src.processing.data_loader import load_transactions_from_db
    from src.processing.transformer import transform_transactions
    from src.processing.feature_engineer import engineer_features
    from src.processing.feature_validator import validate_features

    data = load_transactions_from_db()

    transformed_data = transform_transactions(data)

    feature_data = engineer_features(transformed_data)

    report = validate_features(feature_data)

    if not report["is_valid"]:
        raise ValueError(
            "Feature validation failed. "
            "Processed data will not be saved."
        )

    save_processed_data(feature_data)