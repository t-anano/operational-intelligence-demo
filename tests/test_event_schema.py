
import pytest

from src.event_schema import validate_event


@pytest.fixture
def valid_event():
    return {
        "event_id": "evt-001",
        "timestamp": "2026-10-29T12:00:00Z",
        "service": "checkout-api",
        "metric": "error_rate",
        "value": 8.5,
        "unit": "percent",
        "severity": "warning",
    }


def test_valid_event_is_accepted(valid_event):
    assert validate_event(valid_event) is None


def test_missing_field_is_rejected(valid_event):
    del valid_event["service"]

    with pytest.raises(ValueError, match="Missing required fields"):
        validate_event(valid_event)


def test_timestamp_without_timezone_is_rejected(valid_event):
    valid_event["timestamp"] = "2026-10-29T12:00:00"

    with pytest.raises(ValueError, match="timezone"):
        validate_event(valid_event)


def test_non_finite_value_is_rejected(valid_event):
    valid_event["value"] = float("nan")

    with pytest.raises(ValueError, match="finite"):
        validate_event(valid_event)


def test_invalid_severity_is_rejected(valid_event):
    valid_event["severity"] = "urgent"

    with pytest.raises(ValueError, match="severity"):
        validate_event(valid_event)
