# \# Operational Intelligence Demo

# 

# A Python and Streamlit prototype that transforms simulated operational telemetry into explainable incidents and recommended investigative actions.

# 

# \*\*Live demo:\*\* https://t-anano-operational-intelligence-demo-app-crkdfp.streamlit.app/  

# \*\*Source code:\*\* https://github.com/t-anano/operational-intelligence-demo

# 

# \## Problem

# 

# Operational teams need to distinguish meaningful service degradation from routine telemetry. This prototype demonstrates a simple, transparent workflow for identifying elevated error rates, presenting supporting evidence, and guiding an operator toward an initial investigation.

# 

# \## Current capabilities

# 

# \- Generate repeatable simulated telemetry events.

# \- Validate event records, including required fields, timestamps, numeric values, and severity.

# \- Detect error-rate events that exceed a configurable threshold.

# \- Group elevated events into an incident summary.

# \- Report affected-event count, peak error rate, incident time window, and supporting evidence.

# \- Recommend an initial investigation step.

# \- Display telemetry and incident summaries in an interactive Streamlit dashboard.

# \- Test event validation and incident detection with pytest.

# 

# \## Technology

# 

# \- Python

# \- Streamlit

# \- pytest

# \- Structured event data

# 

# \## Run locally

# 

# Clone the repository and navigate to the project directory:

# 

# ```bash

# git clone https://github.com/t-anano/operational-intelligence-demo.git

# cd operational-intelligence-demo

# ```

# 

# Create and activate a virtual environment, then install the project dependencies listed in `requirements.txt`:

# 

# ```bash

# python -m venv .venv

# ```

# 

# Windows PowerShell:

# 

# ```powershell

# .\\.venv\\Scripts\\Activate.ps1

# pip install -r requirements.txt

# ```

# 

# Run the automated tests:

# 

# ```bash

# python -m pytest -q

# ```

# 

# Launch the dashboard:

# 

# ```bash

# streamlit run app.py

# ```

# 

# \## Demonstration scenario

# 

# The included simulated dataset contains a checkout API error-rate spike. At the default 5.0% threshold, the detector identifies five elevated events and reports a peak error rate of 8.95%.

# 

# The dashboard lets the user adjust the threshold to explore how alert sensitivity affects incident detection.

# 

# \## Limitations

# 

# \- All telemetry is simulated and deterministic.

# \- The prototype is not connected to production systems or live monitoring infrastructure.

# \- Detection uses a configurable error-rate threshold; it does not establish root cause.

# \- Recommended actions are investigative suggestions, not verified diagnoses or automated remediation.

# 

# \## Future improvements

# 

# \- Add visual trend comparisons between baseline and elevated telemetry.

# \- Expand incident grouping and severity prioritization.

# \- Add tests for invalid thresholds and additional event edge cases.

# \- Record a short walkthrough showing the dashboard and its incident-triage workflow.

# 

# \## Project status

# 

# \*\*Working prototype.\*\* The dashboard is deployed, the core detection workflow is implemented, and the current automated test suite passes.

# 

