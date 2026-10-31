
import streamlit as st
import pandas as pd
from datetime import datetime, timezone

from src.detect_incidents import detect_incidents
from src.generate_events import generate_events


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Operational Intelligence | Command Center",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM DESIGN SYSTEM
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #0b1118;
        --panel: #111b26;
        --panel-alt: #152230;
        --border: #263746;
        --text: #e8eef4;
        --muted: #91a2b2;
        --blue: #65b8e8;
        --green: #55c59a;
        --amber: #e5ad58;
        --red: #ed7777;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: var(--bg);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: rgba(11, 17, 24, 0.95);
    }

    [data-testid="stSidebar"] {
        background-color: #0e1822;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
        color: var(--text);
    }

    .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: var(--text) !important;
        letter-spacing: -0.035em;
    }

    p, label {
        color: var(--text);
    }

    .eyebrow {
        color: var(--muted);
        font-family: 'DM Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .command-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        padding: 1.1rem 1.35rem;
        background: linear-gradient(110deg, #142535, #111b26);
        border: 1px solid var(--border);
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }

    .brand {
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: 0.035em;
        color: #f1f6fa;
    }

    .brand-mark {
        color: var(--blue);
        margin-right: 0.55rem;
    }

    .system-status {
        color: var(--green);
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.08em;
        border: 1px solid #285d4e;
        background: #142b28;
        border-radius: 5px;
        padding: 0.4rem 0.65rem;
        white-space: nowrap;
    }

    .metric-card {
        background: linear-gradient(145deg, #152332, #111b26);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1rem 1.1rem;
        min-height: 112px;
    }

    .metric-label {
        color: var(--muted);
        font-size: 0.68rem;
        font-family: 'DM Mono', monospace;
        letter-spacing: 0.09em;
        text-transform: uppercase;
    }

    .metric-value {
        color: #f1f5f9;
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 0.45rem;
        letter-spacing: -0.05em;
    }

    .metric-note {
        color: var(--muted);
        font-size: 0.72rem;
        margin-top: 0.2rem;
    }

    .section-heading {
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.09em;
        color: #dce6ee;
        text-transform: uppercase;
        margin: 1.6rem 0 0.85rem 0;
    }

    .panel {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.8rem;
    }

    .incident-title {
        font-size: 1rem;
        font-weight: 700;
        color: #f1f5f9;
    }

    .incident-meta {
        font-family: 'DM Mono', monospace;
        font-size: 0.68rem;
        color: var(--muted);
        margin-top: 0.35rem;
    }

    .status-pill {
        display: inline-block;
        padding: 0.28rem 0.55rem;
        border-radius: 5px;
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.07em;
        font-family: 'DM Mono', monospace;
    }

    .status-high {
        background: #3b2225;
        border: 1px solid #794044;
        color: #f08c8c;
    }

    .status-warning {
        background: #382e1e;
        border: 1px solid #70572e;
        color: #e8b969;
    }

    .status-healthy {
        background: #17342c;
        border: 1px solid #316a56;
        color: #71d4a9;
    }

    .evidence-item {
        border-left: 2px solid #4a94bb;
        padding: 0.45rem 0.75rem;
        margin: 0.45rem 0;
        background: #142230;
        color: #cbd8e2;
        font-size: 0.83rem;
    }

    .response-step {
        padding: 0.65rem 0.8rem;
        margin: 0.45rem 0;
        background: #142230;
        border: 1px solid #263b4c;
        border-radius: 6px;
        color: #d5e0e9;
        font-size: 0.82rem;
    }

    .footer-note {
        border-top: 1px solid var(--border);
        padding-top: 1rem;
        margin-top: 2.5rem;
        color: var(--muted);
        font-size: 0.7rem;
        font-family: 'DM Mono', monospace;
    }

    div[data-testid="stMetric"] {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 9px;
        padding: 0.8rem;
    }

    div[data-testid="stMetricLabel"] {
        color: var(--muted);
    }

    div[data-testid="stMetricValue"] {
        color: var(--text);
    }

    div[data-testid="stPlotlyChart"],
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 9px;
        overflow: hidden;
    }

    .stButton > button {
        background: #19364b;
        color: #e8f3fa;
        border: 1px solid #315c77;
        border-radius: 6px;
    }

    .stButton > button:hover {
        background: #234b65;
        color: white;
        border-color: var(--blue);
    }

    [data-testid="stExpander"] {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR — MONITORING CONFIGURATION
# ============================================================

with st.sidebar:
    st.markdown(
        '<div class="eyebrow">CONTROL PANEL</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Monitoring Configuration")

    threshold = st.slider(
        "Error-rate threshold (%)",
        min_value=1.0,
        max_value=10.0,
        value=5.0,
        step=0.5,
    )

    st.markdown("---")

    st.markdown(
        '<div class="eyebrow">ENVIRONMENT</div>',
        unsafe_allow_html=True,
    )

    st.selectbox(
        "Environment",
        ["Simulation — Environment 01"],
        disabled=True,
    )

    st.markdown("---")

    st.markdown(
        '<div class="eyebrow">DETECTION RULE</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "An incident is identified when one or more "
        "error-rate events exceed the configured threshold."
    )

    st.markdown("---")

    st.markdown(
        '<div class="eyebrow">DATA SOURCE</div>',
        unsafe_allow_html=True,
    )

    st.caption("Simulated operational telemetry")

    st.markdown(
        """
        <div style="
            color:#91a2b2;
            font-size:0.68rem;
            font-family:'DM Mono',monospace;
            margin-top:2rem;">
            OPERATIONAL INTELLIGENCE<br>
            COMMAND CENTER v2.0
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# DATA INGESTION AND VALIDATION
# ============================================================

# IMPORTANT:
# Keep the original event dictionaries unchanged.
# The detector validates ISO 8601 timestamp strings.

events = generate_events()

incidents = detect_incidents(
    events,
    error_rate_threshold=threshold,
)

# DataFrame is only for display and visualization.
events_df = pd.DataFrame(events)

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

# Use the highest-priority incident for the overview.
selected_incident = incidents[0] if incidents else None


# ============================================================
# COMMAND HEADER
# ============================================================

status_text = (
    "INCIDENTS DETECTED"
    if incidents
    else "MONITORING ACTIVE"
)

status_class = (
    "status-warning"
    if incidents
    else "status-healthy"
)

st.markdown(
    f"""
    <div class="command-header">
        <div>
            <div class="brand">
                <span class="brand-mark">◈</span>
                OPERATIONAL INTELLIGENCE
            </div>
            <div class="eyebrow" style="margin-top:0.45rem;">
                COMMAND CENTER / SIMULATION ENVIRONMENT 01
            </div>
        </div>
        <div class="system-status">
            ● {status_text}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="eyebrow">OPERATIONAL OVERVIEW</div>',
    unsafe_allow_html=True,
)

st.title("Situation Overview")

st.caption(
    "A consolidated view of telemetry, service health, "
    "and detected operational incidents."
)


# ============================================================
# KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Events Received</div>
            <div class="metric-value">{len(events):,}</div>
            <div class="metric-note">Total telemetry records</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Incidents Detected</div>
            <div class="metric-value">{len(incidents):,}</div>
            <div class="metric-note">Current detection window</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Peak Error Rate</div>
            <div class="metric-value">{peak_error_rate:.2f}%</div>
            <div class="metric-note">Highest observed value</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Alert Threshold</div>
            <div class="metric-value">{threshold:.1f}%</div>
            <div class="metric-note">Configured detection rule</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# MAIN OPERATIONS WORKSPACE
# ============================================================

st.markdown(
    '<div class="section-heading">01 / Operational Monitoring</div>',
    unsafe_allow_html=True,
)

left_col, right_col = st.columns(
    [1.65, 1],
    gap="large",
)


# ------------------------------------------------------------
# TELEMETRY CHART
# ------------------------------------------------------------

with left_col:
    st.markdown("### Telemetry Trend")

    st.caption(
        "Error-rate observations compared against the active alert threshold."
    )

    if error_rate_events:
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
            "Blue: observed error rate · "
            "Orange: configured threshold"
        )

    else:
        st.info("No error-rate events are available.")


# ------------------------------------------------------------
# INCIDENT FEED
# ------------------------------------------------------------

with right_col:
    st.markdown("### Incident Feed")

    st.caption(
        "Detected conditions requiring operational attention."
    )

    if incidents:
        for index, incident in enumerate(incidents):
            priority = incident["priority"].upper()

            pill_class = (
                "status-high"
                if priority == "HIGH"
                else "status-warning"
            )

            st.markdown(
                f"""
                <div class="panel">
                    <div style="
                        display:flex;
                        justify-content:space-between;
                        align-items:center;
                        gap:0.5rem;">
                        <span class="incident-title">
                            {incident['service']}
                        </span>
                        <span class="status-pill {pill_class}">
                            {priority}
                        </span>
                    </div>
                    <div class="incident-meta">
                        {incident['incident_id']}
                        &nbsp;·&nbsp;
                        {incident['affected_event_count']} elevated events
                    </div>
                    <div style="
                        color:#e8eef4;
                        font-size:1.25rem;
                        font-weight:700;
                        margin-top:0.8rem;">
                        {incident['peak_value_percent']:.2f}%
                    </div>
                    <div class="incident-meta">
                        PEAK ERROR RATE
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander(
                f"Investigate incident {index + 1}",
                expanded=(index == 0),
            ):
                st.write(incident["impact_summary"])

                st.write("**Incident window**")

                st.caption(
                    f"{incident['first_seen']} → "
                    f"{incident['last_seen']}"
                )

                st.write("**Evidence**")

                for item in incident["evidence"]:
                    st.markdown(
                        f'<div class="evidence-item">{item}</div>',
                        unsafe_allow_html=True,
                    )

                st.write("**Recommended investigation**")
                st.write(incident["recommended_action"])

    else:
        st.markdown(
            """
            <div class="panel">
                <span class="status-pill status-healthy">
                    NO ACTIVE INCIDENTS
                </span>
                <div style="
                    font-size:0.95rem;
                    color:#e8eef4;
                    font-weight:600;
                    margin-top:0.9rem;">
                    Monitoring within configured limits
                </div>
                <div class="incident-meta">
                    No error-rate events exceeded the selected threshold.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# OPERATIONAL ASSESSMENT
# ============================================================

st.markdown(
    '<div class="section-heading">02 / Operational Assessment</div>',
    unsafe_allow_html=True,
)

if selected_incident:
    assessment_left, assessment_right = st.columns(
        [1.2, 1],
        gap="large",
    )

    with assessment_left:
        st.markdown("### Situation Assessment")

        st.markdown(
            f"""
            <div class="panel">
                <div class="eyebrow">OBSERVED CONDITION</div>
                <div style="
                    font-size:1.05rem;
                    font-weight:700;
                    color:#f1f5f9;
                    margin-bottom:0.8rem;">
                    {selected_incident['service']} — Elevated Error Rate
                </div>
                <div style="color:#cbd8e2;font-size:0.86rem;">
                    {selected_incident['impact_summary']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("**Assessment details**")

        st.write(
            f"- Affected events: "
            f"{selected_incident['affected_event_count']}"
        )

        st.write(
            f"- Peak observed rate: "
            f"{selected_incident['peak_value_percent']:.2f}%"
        )

        st.write(
            f"- Configured threshold: "
            f"{selected_incident['threshold_percent']:.1f}%"
        )

    with assessment_right:
        st.markdown("### Initial Response Plan")

        response_steps = [
            "Inspect service logs during the incident window.",
            "Check recent deployments and dependency health.",
            "Compare observed error rates with the configured threshold.",
            "Determine whether customer-facing workflows are affected.",
            "Reassess severity after collecting additional evidence.",
        ]

        for number, step in enumerate(response_steps, start=1):
            st.markdown(
                f"""
                <div class="response-step">
                    <span style="
                        color:#65b8e8;
                        font-family:'DM Mono',monospace;
                        font-weight:700;">
                        {number:02d}
                    </span>
                    &nbsp;&nbsp;{step}
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.warning(
        "Assessment is based on simulated telemetry. "
        "Customer impact, root cause, and remediation are not independently verified."
    )

else:
    st.markdown(
        """
        <div class="panel">
            <span class="status-pill status-healthy">
                NORMAL OPERATING CONDITION
            </span>
            <p style="margin-top:0.8rem;color:#cbd8e2;">
                No incidents were identified by the current
                threshold-based detection rule.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# TELEMETRY EXPLORER
# ============================================================

st.markdown(
    '<div class="section-heading">03 / Telemetry Explorer</div>',
    unsafe_allow_html=True,
)

with st.expander(
    "Explore raw telemetry records",
    expanded=False,
):
    available_services = sorted(
        events_df["service"].dropna().unique().tolist()
    )

    selected_services = st.multiselect(
        "Filter by service",
        options=available_services,
        default=available_services,
    )

    available_metrics = sorted(
        events_df["metric"].dropna().unique().tolist()
    )

    selected_metrics = st.multiselect(
        "Filter by metric",
        options=available_metrics,
        default=available_metrics,
    )

    filtered_df = events_df[
        events_df["service"].isin(selected_services)
        & events_df["metric"].isin(selected_metrics)
    ].copy()

    display_columns = [
        "event_id",
        "timestamp",
        "service",
        "metric",
        "value",
        "unit",
        "severity",
    ]

    available_columns = [
        column
        for column in display_columns
        if column in filtered_df.columns
    ]

    filtered_df = filtered_df[available_columns]

    filtered_df = filtered_df.rename(
        columns={
            "event_id": "Event ID",
            "timestamp": "Timestamp (UTC)",
            "service": "Service",
            "metric": "Metric",
            "value": "Value",
            "unit": "Unit",
            "severity": "Source Severity",
        }
    )

    st.caption(
        f"Showing {len(filtered_df):,} of {len(events_df):,} records."
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# METHODOLOGY
# ============================================================

with st.expander("Detection methodology and limitations"):
    st.markdown(
        """
        **Telemetry ingestion**

        Events are generated using a simulated data source and
        validated against the project's event schema.

        **Incident detection**

        The current detector identifies error-rate events that
        exceed a user-configured threshold and groups elevated
        observations into an incident.

        **Evidence**

        Incident summaries report observed event counts, peak
        error rates, and the configured threshold.

        **Limitations**

        - The application is not connected to production infrastructure.
        - Threshold detection does not independently establish root cause.
        - Customer impact is not independently verified.
        - Recommended actions are investigation suggestions.
        - Human review is required before operational decisions.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-note">
        OPERATIONAL INTELLIGENCE · COMMAND CENTER v2.0
        <br><br>
        SIMULATED TELEMETRY &nbsp;|&nbsp;
        SCHEMA-VALIDATED EVENTS &nbsp;|&nbsp;
        HUMAN-IN-THE-LOOP INVESTIGATION
    </div>
    """,
    unsafe_allow_html=True,
)
