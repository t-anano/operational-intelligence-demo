# Operational Event Schema

## Purpose

Define a consistent structure for simulated telemetry events so they can be validated, analyzed, and converted into actionable incidents.

## Required fields

| Field | Type | Description |
|---|---|---|
| event_id | string | Unique event identifier |
| timestamp | ISO 8601 string | Time the event occurred, including timezone |
| service | string | Service producing the event |
| metric | string | Metric being observed |
| value | number | Observed metric value |
| unit | string | Unit of measurement |
| severity | string | Source event severity: info, warning, or critical |

## Example event

```json
{
  "event_id": "evt-001",
  "timestamp": "2026-10-29T12:00:00Z",
  "service": "checkout-api",
  "metric": "error_rate",
  "value": 8.5,
  "unit": "percent",
  "severity": "warning"
}
```

## Validation rules

- Every required field must be present.
- `event_id`, `service`, `metric`, and `unit` must be non-empty strings.
- `timestamp` must be a valid ISO 8601 timestamp with timezone information.
- `value` must be a finite number.
- `severity` must be one of `info`, `warning`, or `critical`.
- Invalid events must be rejected with a useful error message rather than silently accepted.

## Initial detection scenario

Simulate an increase in the checkout API's error rate. The system should identify the abnormal behavior, explain which observations support the alert, assign an incident priority, and suggest an investigation step.

All events and thresholds will be simulated for demonstration purposes, not derived from a live production system.
