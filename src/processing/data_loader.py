import pandas as pd
from sqlalchemy import text

from src.utils.database import get_engine


def load_transactions_from_db() -> pd.DataFrame:
    engine = get_engine()

    query = text("""
        SELECT
            order_id,
            customer_id,
            product_id,
            order_date,
            quantity,
            unit_price,
            discount,
            region,
            payment_method
        FROM transactions
        ORDER BY order_id;
    """)

    with engine.connect() as connection:
        data = pd.read_sql(query, connection)

    return data


if __name__ == "__main__":
    data = load_transactions_from_db()

    print(f"Loaded {len(data)} transactions from PostgreSQL.")
    print(f"Columns: {len(data.columns)}")
    print("\nSample:")
    print(data.head())