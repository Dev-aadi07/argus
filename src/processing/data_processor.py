from pathlib import Path

import pandas as pd


def separate_data(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:

    valid_data = data[data["is_valid"]].copy()

    invalid_data = data[~data["is_valid"]].copy()

    return valid_data, invalid_data


def save_processed_data(
    valid_data: pd.DataFrame,
    invalid_data: pd.DataFrame
):
    processed_path = Path(
        "data/processed/valid_transactions.csv"
    )

    quarantine_path = Path(
        "data/quarantine/invalid_transactions.csv"
    )

    processed_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    quarantine_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    valid_data.to_csv(
        processed_path,
        index=False
    )

    invalid_data.to_csv(
        quarantine_path,
        index=False
    )

    return processed_path, quarantine_path