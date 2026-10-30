import streamlit as st
import pandas as pd

from src.detect_incidents import detect_incidents
from src.generate_events import generate_events


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Operational Intelligence",
    page_icon="🔎",
    layout="wide",
)

st.title("Operational Intelligence")
st.caption(
    "Simulated telemetry monitoring, incident detection, "
    "and operational triage"
)


# --------------------------------------------------
# Sidebar configuration
# --------------------------------------------------

st.sidebar.header("Monitoring Configuration")

threshold = st.sidebar.slider(
    "Error-rate alert threshold (%)",
    min_value=1.0,
    max_value=10.0,
    value=5.0,
    step=0.5,
)

st.sidebar.caption(
    "Adjust the threshold to explore how incident detection changes."
)


# --------------------------------------------------
# Generate telemetry and detect incidents
# --------------------------------------------------

# Keep the original event dictionaries intact.
# The timestamp strings are required by validate_event().
events = generate_events()

incidents = detect_incidents(
    events,
    error_rate_threshold=threshold,
)

# Create a separate DataFrame for tables and visualizations.
# Never pass this DataFrame back to detect_incidents().
events_df = pd.DataFrame(events)


# --------------------------------------------------
# Key performance indicators
# --------------------------------------------------

error_rate_events = [
    event
    for event in events
    if event["metric"] == "error_rate"
]

peak_error_rate = (
    max(event["value"] for event in error_rate_events)
    if error_rate_events
    else 0.0
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Events Received",
    len(events),
)

col2.metric(
    "Incidents Detected",
    len(incidents),
)

col3.metric(
    "Peak Error Rate",
    f"{peak_error_rate:.2f}%",
)


# --------------------------------------------------
# Telemetry visualization
# --------------------------------------------------

st.subheader("Error Rate Over Time")

if error_rate_events:
    # Build the chart from the original events.
    # Convert timestamps only in the separate chart DataFrame.
    chart_df = pd.DataFrame(
        [
            {
                "Time": event["timestamp"],
                "Error rate (%)": event["value"],
            }
            for event in error_rate_events
        ]
    )

    chart_df["Time"] = pd.to_datetime(
        chart_df["Time"],
        utc=True,
    )

    chart_df = chart_df.sort_values("Time")

    # Include the configured threshold as a chart series.
    chart_df["Alert threshold (%)"] = threshold

    chart_df = chart_df.set_index("Time")

    st.line_chart(
        chart_df[
            [
                "Error rate (%)",
                "Alert threshold (%)",
            ]
        ],
        use_container_width=True,
    )

    st.caption(
        f"The horizontal reference represents the configured "
        f"{threshold:.1f}% alert threshold. "
        "Only error-rate events are included in this chart."
    )

else:
    st.info("No error-rate telemetry events are available to chart.")


# --------------------------------------------------
# Telemetry event table
# --------------------------------------------------

st.subheader("Telemetry Events")

with st.expander("Inspect individual telemetry events", expanded=True):
    display_columns = {
        "event_id": "Event ID",
        "timestamp": "Time (UTC)",
        "service": "Service",
        "metric": "Metric",
        "value": "Value",
        "unit": "Unit",
        "severity": "Source Severity",
    }

    available_columns = [
        column
        for column in display_columns
        if column in events_df.columns
    ]

    display_df = events_df[available_columns].rename(
        columns=display_columns
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )


# --------------------------------------------------
# Operational summary
# --------------------------------------------------

st.subheader("Operational Summary")

if incidents:
    incident = incidents[0]

    st.write("**Customer impact assessment**")
    st.write(incident["impact_summary"])

    st.write(
        f"The **{incident['service']}** service recorded "
        f"**{incident['affected_event_count']}** elevated "
        f"error-rate events. The peak observed error rate was "
        f"**{incident['peak_value_percent']:.2f}%**, compared "
        f"with the configured threshold of "
        f"**{incident['threshold_percent']:.1f}%**."
    )

    st.caption(
        "These findings are based on simulated telemetry. "
        "Customer impact has not been independently verified."
    )

else:
    st.success(
        "No incidents detected at the selected threshold."
    )

    st.write(
        "Continue monitoring telemetry for changes. "
        "No incident was identified by the current detection rules."
    )


# --------------------------------------------------
# Incident triage
# --------------------------------------------------

st.subheader("Incident Triage")

if incidents:
    for incident in incidents:
        with st.container(border=True):
            st.error(
                f"{incident['priority'].upper()} PRIORITY — "
                f"{incident['service']}"
            )

            metric_col1, metric_col2, metric_col3 = st.columns(3)

            metric_col1.metric(
                "Peak Error Rate",
                f"{incident['peak_value_percent']:.2f}%",
            )

            metric_col2.metric(
                "Affected Events",
                incident["affected_event_count"],
            )

            metric_col3.metric(
                "Alert Threshold",
                f"{incident['threshold_percent']:.1f}%",
            )

            st.write("**Incident Window**")

            st.write(
                f"{incident['first_seen']} → "
                f"{incident['last_seen']}"
            )

            st.write("**Supporting Evidence**")

            for item in incident["evidence"]:
                st.markdown(f"- {item}")

            st.write("**Recommended Investigation**")
            st.write(incident["recommended_action"])

            st.write("**Initial Response Plan**")

            st.markdown(
                """
                1. Inspect service logs during the incident window.
                2. Check recent deployments and dependency health.
                3. Compare observed error rates against the configured threshold.
                4. Determine whether the issue affects customer-facing workflows.
                5. Reassess incident severity after gathering additional evidence.
                """
            )

            st.warning(
                "The recommended actions are investigation suggestions, "
                "not verified root causes or confirmed remediations."
            )

else:
    st.info(
        "There are no incidents to triage at the selected threshold. "
        "Try lowering the threshold to explore the detector's behavior."
    )


# --------------------------------------------------
# Methodology and limitations
# --------------------------------------------------

with st.expander("About this demo"):
    st.markdown(
        """
        **Purpose**

        Demonstrate a small operational intelligence workflow:
        telemetry ingestion, schema validation, threshold-based
        incident detection, and evidence-based triage.

        **Detection logic**

        An incident is identified when one or more error-rate events
        exceed the configured threshold.

        **Limitations**

        - Telemetry is simulated, not sourced from production systems.
        - Threshold-based detection does not establish root cause.
        - Customer impact is not independently verified.
        - Recommended actions require investigation and human judgment.
        """
    )

st.caption(
    "Operational Intelligence Demo · Simulated data only · "
    "Not connected to production systems"
)
