import pandas as pd
import pytest

from src.ingestion.csv_ingestion import load_csv
from src.processing.validator import validate_data
from src.processing.data_processor import separate_data


DATA_PATH = "data/raw/ecommerce_transactions.csv"


def test_csv_ingestion():
    data, metadata = load_csv(DATA_PATH)

    assert isinstance(data, pd.DataFrame)
    assert metadata["rows"] == 15
    assert metadata["columns"] == 9


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        load_csv("data/raw/does_not_exist.csv")


def test_validation_detects_invalid_records():
    data, _ = load_csv(DATA_PATH)

    validated_data, report = validate_data(data)

    assert report["total_records"] == 15
    assert report["invalid_records"] == 5
    assert report["valid_records"] == 10


def test_validation_marks_invalid_rows():
    data, _ = load_csv(DATA_PATH)

    validated_data, _ = validate_data(data)

    invalid_data = validated_data[
        ~validated_data["is_valid"]
    ]

    assert len(invalid_data) == 5


def test_separation():
    data, _ = load_csv(DATA_PATH)

    validated_data, _ = validate_data(data)

    valid_data, invalid_data = separate_data(
        validated_data
    )

    assert len(valid_data) == 10
    assert len(invalid_data) == 5

def test_validation_does_not_modify_raw_data():
    data, _ = load_csv(DATA_PATH)

    original = data.copy(deep=True)

    validate_data(data)

    pd.testing.assert_frame_equal(
        data,
        original
    )