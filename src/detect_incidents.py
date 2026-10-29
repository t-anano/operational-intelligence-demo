
from src.event_schema import validate_event


def detect_incidents(
    events: list[dict],
    error_rate_threshold: float = 5.0,
) -> list[dict]:
    """Identify high error-rate events and group them into one incident."""
    if error_rate_threshold < 0:
        raise ValueError("Threshold must be non-negative")

    for event in events:
        validate_event(event)

    elevated = [
        event
        for event in events
        if event["metric"] == "error_rate"
        and event["value"] > error_rate_threshold
    ]

    if not elevated:
        return []

    peak_event = max(elevated, key=lambda event: event["value"])

    return [{
        "incident_id": "inc-001",
        "service": peak_event["service"],
        "metric": "error_rate",
        "priority": "high",
        "threshold_percent": error_rate_threshold,
        "affected_event_count": len(elevated),
        "peak_value_percent": peak_event["value"],
        "first_seen": min(e["timestamp"] for e in elevated),
        "last_seen": max(e["timestamp"] for e in elevated),
        "evidence": [
            f"{len(elevated)} events exceeded the "
            f"{error_rate_threshold}% error-rate threshold",
            f"Peak observed error rate: {peak_event['value']}%",
        ],
        "recommended_action": (
            "Inspect checkout API logs and recent deployments; verify whether "
"the elevated error rate correlates with a recent release or "
"dependency failure.; "
            "verify whether the elevated error rate is ongoing."
        ),
    }]
