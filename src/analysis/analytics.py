import pandas as pd
from sqlalchemy import text

from src.utils.database import get_engine


def get_region_summary() -> pd.DataFrame:
    engine = get_engine()

    query = text("""
        SELECT
            region,
            COUNT(*) AS transaction_count,
            SUM(quantity) AS total_units,
            ROUND(
                SUM(quantity * unit_price * (1 - discount)),
                2
            ) AS total_revenue
        FROM transactions
        GROUP BY region
        ORDER BY total_revenue DESC;
    """)

    with engine.connect() as connection:
        return pd.read_sql(query, connection)


def get_product_summary() -> pd.DataFrame:
    engine = get_engine()

    query = text("""
        SELECT
            product_id,
            SUM(quantity) AS units_sold
        FROM transactions
        GROUP BY product_id
        ORDER BY units_sold DESC;
    """)

    with engine.connect() as connection:
        return pd.read_sql(query, connection)


def get_payment_summary() -> pd.DataFrame:
    engine = get_engine()

    query = text("""
        SELECT
            payment_method,
            SUM(
                quantity * unit_price * (1 - discount)
            ) AS revenue
        FROM transactions
        GROUP BY payment_method
        ORDER BY revenue DESC;
    """)

    with engine.connect() as connection:
        return pd.read_sql(query, connection)
      
def get_overall_summary() -> dict:
    engine = get_engine()

    query = text("""
        SELECT
            COUNT(*) AS total_transactions,
            SUM(quantity) AS total_units,
            ROUND(
                SUM(quantity * unit_price * (1 - discount)),
                2
            ) AS total_revenue
        FROM transactions;
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().one()

    return dict(result)


if __name__ == "__main__":
    print("\n=== OVERALL SUMMARY ===")
    print(get_overall_summary())

    print("\n=== REGION ANALYSIS ===")
    print(get_region_summary())

    print("\n=== PRODUCT ANALYSIS ===")
    print(get_product_summary())

    print("\n=== PAYMENT ANALYSIS ===")
    print(get_payment_summary())