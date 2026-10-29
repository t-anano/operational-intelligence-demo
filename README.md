## \# Operational Intelligence Demo

## 

## A Python and Streamlit prototype that transforms simulated operational telemetry into explainable incidents and recommended investigative actions.

## 

## \*\*Live Demo:\*\* \[Operational Intelligence Dashboard](https://t-anano-operational-intelligence-demo-app-crkdfp.streamlit.app/)  

## \*\*Source Code:\*\* \[GitHub Repository](https://github.com/t-anano/operational-intelligence-demo)

## 

## \## Problem

## 

## Operational teams need to distinguish meaningful service degradation from routine telemetry. This prototype demonstrates a simple, transparent workflow for identifying elevated error rates, presenting supporting evidence, and guiding an operator toward an initial investigation.

## 

## \## Current Capabilities

## 

## \- Generate repeatable simulated telemetry events.

## \- Validate event records, including required fields, timestamps, numeric values, and severity.

## \- Detect error-rate events that exceed a configurable threshold.

## \- Group elevated events into an incident summary.

## \- Report affected-event count, peak error rate, incident time window, and supporting evidence.

## \- Recommend an initial investigation step.

## \- Display telemetry and incident summaries in an interactive Streamlit dashboard.

## \- Test event validation and incident detection with pytest.

## 

## \## Technology Stack

## 

## \- \*\*Python\*\* — event processing and incident detection

## \- \*\*Streamlit\*\* — interactive dashboard

## \- \*\*pytest\*\* — automated testing

## \- \*\*Structured event data\*\* — simulated telemetry input

## 

## \## Run Locally

## 

## \### 1. Clone the repository

## 

## ```bash

## git clone https://github.com/t-anano/operational-intelligence-demo.git

## cd operational-intelligence-demo

## ```

## 

## \### 2. Create a virtual environment

## 

## ```bash

## python -m venv .venv

## ```

## 

## \### 3. Activate the virtual environment

## 

## On Windows PowerShell:

## 

## ```powershell

## .\\.venv\\Scripts\\Activate.ps1

## ```

## 

## \### 4. Install dependencies

## 

## ```bash

## pip install -r requirements.txt

## ```

## 

## \### 5. Run the automated tests

## 

## ```bash

## python -m pytest -q

## ```

## 

## \### 6. Launch the dashboard

## 

## ```bash

## streamlit run app.py

## ```

## 

## Streamlit will provide a local URL where you can interact with the dashboard.

## 

## \## Demonstration Scenario

## 

## The included simulated dataset contains an elevated checkout API error rate. At the default \*\*5.0% threshold\*\*, the detector identifies five elevated events and reports a peak error rate of \*\*8.95%\*\*.

## 

## The interactive dashboard allows users to adjust the threshold and observe how alert sensitivity affects incident detection.

## 

## \## Limitations

## 

## \- All telemetry is simulated and deterministic.

## \- The prototype is not connected to production systems or live monitoring infrastructure.

## \- Detection uses a configurable error-rate threshold and does not establish root cause.

## \- Recommended actions are investigative suggestions, not verified diagnoses or automated remediation.

## 

## \## Future Improvements

## 

## \- Add visual trend comparisons between baseline and elevated telemetry.

## \- Expand incident grouping and severity prioritization.

## \- Add tests for invalid thresholds and additional event edge cases.

## \- Record a short walkthrough demonstrating the workflow from telemetry input to incident triage.

## 

## \## Project Status

## 

## \*\*Working prototype.\*\* The dashboard is deployed, the core detection workflow is implemented, and the current automated test suite passes.



