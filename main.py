from src.ingestion.csv_ingestion import load_csv


def main():
    print("================================")
    print("          ARGUS STARTING")
    print("================================")

    data, metadata = load_csv(
        "data/raw/ecommerce_transactions.csv"
    )

    print("\nData ingestion successful.")

    print(f"Rows received: {metadata['rows']}")
    print(f"Columns received: {metadata['columns']}")

    print("\nARGUS received:")
    print(data.head())


if __name__ == "__main__":
    main()