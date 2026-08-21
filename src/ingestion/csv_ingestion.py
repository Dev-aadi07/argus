from datetime import datetime
from pathlib import Path

import pandas as pd


def load_csv(file_path: str) -> tuple[pd.DataFrame, dict]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")

    if path.suffix.lower() != ".csv":
        raise ValueError("Only CSV files are supported currently.")

    data = pd.read_csv(path)

    metadata = {
        "source": str(path),
        "ingested_at": datetime.now().isoformat(),
        "rows": len(data),
        "columns": len(data.columns),
    }

    return data, metadata


if __name__ == "__main__":
    data, metadata = load_csv(
        "data/raw/ecommerce_transactions.csv"
    )

    print("ARGUS INGESTION")
    print("----------------")

    for key, value in metadata.items():
        print(f"{key}: {value}")

    print("\nFirst 5 records:")
    print(data.head())