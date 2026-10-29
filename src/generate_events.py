
from datetime import datetime, timedelta, timezone
import random


def generate_events(seed: int = 42) -> list[dict]:
    """Generate deterministic sample telemetry for a checkout API."""
    rng = random.Random(seed)
    start = datetime(2026, 10, 29, 12, 0, tzinfo=timezone.utc)
    events = []

    # Normal operating period: low error rate.
    for minute in range(10):
        events.append({
            "event_id": f"evt-{minute + 1:03}",
            "timestamp": (start + timedelta(minutes=minute)).isoformat(),
            "service": "checkout-api",
            "metric": "error_rate",
            "value": round(rng.uniform(0.5, 1.5), 2),
            "unit": "percent",
            "severity": "info",
        })

    # Incident period: elevated error rate.
    for minute in range(10, 15):
        events.append({
            "event_id": f"evt-{minute + 1:03}",
            "timestamp": (start + timedelta(minutes=minute)).isoformat(),
            "service": "checkout-api",
            "metric": "error_rate",
            "value": round(rng.uniform(7.0, 10.0), 2),
            "unit": "percent",
            "severity": "warning",
        })

    return events


if __name__ == "__main__":
    for event in generate_events():
        print(event)
