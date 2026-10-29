
import streamlit as st
import pandas as pd

from src.detect_incidents import detect_incidents
from src.generate_events import generate_events

st.set_page_config(
    page_title="Operational Intelligence",
    page_icon="🔎",
    layout="wide",
)

st.title("Operational Intelligence")
st.caption("Simulated telemetry monitoring and incident triage")

threshold = st.sidebar.slider(
    "Error-rate alert threshold (%)",
    min_value=1.0,
    max_value=10.0,
    value=5.0,
    step=0.5,
)

events = generate_events()
incidents = detect_incidents(
    events,
    error_rate_threshold=threshold,
)

col1, col2, col3 = st.columns(3)
col1.metric("Events received", len(events))
col2.metric("Incidents detected", len(incidents))
col3.metric(
    "Peak error rate",
    f"{max(event['value'] for event in events):.2f}%",
)

st.subheader("Telemetry events")
st.dataframe(
    [
        {
            "Time (UTC)": event["timestamp"],
            "Service": event["service"],
            "Metric": event["metric"],
            "Value (%)": event["value"],
            "Source severity": event["severity"],
        }
        for event in events
    ],
    use_container_width=True,
)

st.subheader("Error rate over time")

chart_data = [
    {
        "Time": event["timestamp"],
        "Error rate (%)": event["value"],
        "Alert threshold (%)": threshold,
    }
    for event in events
    if event["metric"] == "error_rate"
]

if chart_data:
    chart_df = pd.DataFrame(chart_data).sort_values("Time")
    st.line_chart(
    chart_df,
    x="Time",
    y=["Error rate (%)", "Alert threshold (%)"],
)
    st.caption(
        f"The selected alert threshold is {threshold:.1f}%. "
        "Use the telemetry table below to inspect individual events."
    )



st.subheader("Operational summary")

if incidents:
    incident = incidents[0]
    st.write("**Customer impact assessment**")
    st.write(incident["impact_summary"])
    st.write(
        f"The {incident['service']} service recorded "
        f"{incident['affected_event_count']} elevated error-rate events. "
        f"The peak error rate was "
        f"{incident['peak_value_percent']:.2f}%, exceeding the "
        f"{incident['threshold_percent']:.1f}% alert threshold."
    )
else:
    st.write(
        "No events exceeded the selected error-rate threshold. "
        "Continue monitoring for changes."
    )

st.subheader("Incident triage")

if incidents:
    for incident in incidents:
        st.error(
            f"{incident['priority'].upper()} PRIORITY — "
            f"{incident['service']}"
        )
        st.write(
            f"**Peak error rate:** "
            f"{incident['peak_value_percent']:.2f}%"
        )
        st.write(
            f"**Affected events:** "
            f"{incident['affected_event_count']}"
        )
        st.write(
            f"**Incident window:** "
            f"{incident['first_seen']} to {incident['last_seen']}"
        )

        st.write("**Evidence**")
        for item in incident["evidence"]:
            st.write(f"- {item}")

        st.write("**Recommended investigation**")
        st.write(incident["recommended_action"])

        st.write("**Initial response plan**")
        st.write(
            "1. Review checkout API logs during the incident window.\n"
            "2. Check recent deployments and dependency health.\n"
            "3. Compare the observed error rate with the configured threshold.\n"
            "4. Reassess severity after gathering evidence; do not assume root cause."
        )
else:
    st.success("No incidents detected at the selected threshold.")

st.caption(
    "This demo uses simulated data and is not connected "
    "to production systems."
)
