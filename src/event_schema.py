
from datetime import datetime
import math


REQUIRED_FIELDS = {
    "event_id",
    "timestamp",
    "service",
    "metric",
    "value",
    "unit",
    "severity",
}

VALID_SEVERITIES = {"info", "warning", "critical"}


def validate_event(event: dict) -> None:
    """Validate one operational telemetry event.

    Raises ValueError when the event is invalid.
    """
    if not isinstance(event, dict):
        raise ValueError("Event must be a dictionary")

    missing = REQUIRED_FIELDS - event.keys()
    if missing:
        raise ValueError(f"Missing required fields: {sorted(missing)}")

    for field in ("event_id", "service", "metric", "unit"):
        if not isinstance(event[field], str) or not event[field].strip():
            raise ValueError(f"{field} must be a non-empty string")

    timestamp = event["timestamp"]
    if not isinstance(timestamp, str):
        raise ValueError("timestamp must be an ISO 8601 string")

    try:
        parsed_timestamp = datetime.fromisoformat(
            timestamp.replace("Z", "+00:00")
        )
    except ValueError as exc:
        raise ValueError("timestamp must be a valid ISO 8601 timestamp") from exc

    if parsed_timestamp.utcoffset() is None:
        raise ValueError("timestamp must include timezone information")

    value = event["value"]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("value must be a number")

    if not math.isfinite(value):
        raise ValueError("value must be finite")

    if event["severity"] not in VALID_SEVERITIES:
        raise ValueError(
            f"severity must be one of: {sorted(VALID_SEVERITIES)}"
        )
