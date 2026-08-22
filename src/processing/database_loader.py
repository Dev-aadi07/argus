import pandas as pd
from sqlalchemy import text

from src.utils.database import get_engine


def load_transactions(data: pd.DataFrame) -> int:
    engine = get_engine()

    records = data.to_dict(orient="records")

    insert_query = text("""
        INSERT INTO transactions (
            order_id,
            customer_id,
            product_id,
            order_date,
            quantity,
            unit_price,
            discount,
            region,
            payment_method
        )
        VALUES (
            :order_id,
            :customer_id,
            :product_id,
            :order_date,
            :quantity,
            :unit_price,
            :discount,
            :region,
            :payment_method
        )
        ON CONFLICT (order_id) DO NOTHING
    """)

    with engine.begin() as connection:
        result = connection.execute(insert_query, records)

    return result.rowcount


def log_ingestion(
    source: str,
    ingested_at: str,
    rows_received: int,
    columns_received: int,
    valid_records: int,
    invalid_records: int,
    quality_score: float
) -> None:

    engine = get_engine()

    insert_query = text("""
        INSERT INTO ingestion_logs (
            source,
            ingested_at,
            rows_received,
            columns_received,
            valid_records,
            invalid_records,
            quality_score
        )
        VALUES (
            :source,
            :ingested_at,
            :rows_received,
            :columns_received,
            :valid_records,
            :invalid_records,
            :quality_score
        )
    """)

    with engine.begin() as connection:
        connection.execute(
            insert_query,
            {
            "source": source,
            "ingested_at": ingested_at,
            "rows_received": int(rows_received),
            "columns_received": int(columns_received),
            "valid_records": int(valid_records),
            "invalid_records": int(invalid_records),
            "quality_score": float(quality_score),
        }
        )

if __name__ == "__main__":
    from datetime import datetime

    from src.ingestion.csv_ingestion import load_csv
    from src.processing.validator import validate_data
    from src.processing.data_processor import separate_data

    data, metadata = load_csv(
        "data/raw/ecommerce_transactions.csv"
    )

    validated_data, report = validate_data(data)

    valid_data, invalid_data = separate_data(
        validated_data
    )

    # Don't insert again — records are already in PostgreSQL.
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