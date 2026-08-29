import pandas as pd


def generate_statistical_profile(
    data: pd.DataFrame,
) -> pd.DataFrame:

    numerical_columns = data.select_dtypes(
        include="number"
    ).columns

    profile = data[numerical_columns].describe().T

    profile["median"] = data[numerical_columns].median()

    profile["missing_values"] = (
        data[numerical_columns]
        .isnull()
        .sum()
    )

    return profile


if __name__ == "__main__":
    from src.processing.data_loader import (
        load_transactions_from_db
    )
    from src.processing.transformer import (
        transform_transactions
    )
    from src.processing.feature_engineer import (
        engineer_features
    )

    data = load_transactions_from_db()

    transformed_data = transform_transactions(data)

    feature_data = engineer_features(
        transformed_data
    )

    profile = generate_statistical_profile(
        feature_data
    )

    print("\n=== ARGUS STATISTICAL PROFILE ===")
    print(profile)