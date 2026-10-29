
import pytest

from src.detect_incidents import detect_incidents
from src.generate_events import generate_events


def test_detects_elevated_error_rate():
    incidents = detect_incidents(generate_events())

    assert len(incidents) == 1
    assert incidents[0]["service"] == "checkout-api"
    assert incidents[0]["priority"] == "high"
    assert incidents[0]["affected_event_count"] == 5
    assert incidents[0]["peak_value_percent"] == 8.95


def test_no_incident_when_all_rates_are_below_threshold():
    events = [
        event
        for event in generate_events()
        if event["value"] < 5.0
    ]

    assert detect_incidents(events) == []


def test_rejects_negative_threshold():
    with pytest.raises(ValueError, match="non-negative"):
        detect_incidents(generate_events(), error_rate_threshold=-1)


def test_rejects_invalid_event():
    events = generate_events()
    events[0]["value"] = float("nan")

    with pytest.raises(ValueError, match="finite"):
        detect_incidents(events)
def test_incident_includes_customer_impact_summary():
    incidents = detect_incidents(generate_events(), error_rate_threshold=5.0)

    assert len(incidents) == 1

    incident = incidents[0]

    assert "impact_summary" in incident
    assert "5" in incident["impact_summary"]
    assert "8.95%" in incident["impact_summary"]
    assert "not been independently verified" in incident["impact_summary"]


def test_event_equal_to_threshold_does_not_trigger_incident():
    events = [
        event
        for event in generate_events()
        if event["metric"] == "error_rate"
    ]

    threshold = events[0]["value"]
    events = [events[0]]

    assert detect_incidents(events, error_rate_threshold=threshold) == []

def test_empty_event_list_returns_no_incidents():
    assert detect_incidents([]) == []