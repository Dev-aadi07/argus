import json
from pathlib import Path

from src.processing.data_loader import load_transactions_from_db
from src.processing.transformer import transform_transactions
from src.processing.feature_engineer import engineer_features

from src.analysis.statistical_profile import (
    generate_statistical_profile
)
from src.analysis.distribution_analysis import (
    analyze_distributions
)
from src.analysis.correlation_analysis import (
    calculate_correlations
)
from src.analysis.outlier_analysis import (
    detect_outliers
)
from src.analysis.statistical_baseline import (
    generate_baseline
)


REPORT_PATH = Path(
    "data/processed/statistical_report.json"
)


def generate_statistical_report(data):

    profile = generate_statistical_profile(data)

    distributions = analyze_distributions(data)

    correlations = calculate_correlations(data)

    outliers = detect_outliers(
        data,
        "net_amount"
    )

    baseline = generate_baseline(data)

    report = {
        "dataset": {
            "rows": len(data),
            "columns": len(data.columns),
        },

        "profile": profile.reset_index().to_dict(
            orient="records"
        ),

        "distributions": distributions,

        "correlations": correlations.round(
            4
        ).to_dict(),

        "outliers": {
            "column": "net_amount",
            "count": len(outliers),
            "order_ids": (
                outliers["order_id"]
                .tolist()
            ),
        },

        "baseline": baseline,
    }

    return report


def save_report(report):

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        REPORT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
            default=str
        )

    print(
        f"\nStatistical report saved to "
        f"{REPORT_PATH}"
    )


if __name__ == "__main__":

    data = load_transactions_from_db()

    transformed_data = transform_transactions(
        data
    )

    feature_data = engineer_features(
        transformed_data
    )

    report = generate_statistical_report(
        feature_data
    )

    print("\n=== ARGUS STATISTICAL REPORT ===")

    print(
        f"Records analyzed: "
        f"{report['dataset']['rows']}"
    )

    print(
        f"Columns analyzed: "
        f"{report['dataset']['columns']}"
    )

    print(
        f"Net amount outliers: "
        f"{report['outliers']['count']}"
    )

    save_report(report)