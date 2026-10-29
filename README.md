# Operational Intelligence Demo

## Purpose

A Python-based operational intelligence prototype that turns simulated operational events into prioritized incidents and actionable recommendations.

The goal is to demonstrate how an engineer can transform raw data into a workflow that helps an operator identify, investigate, and respond to problems.

## Problem

Operational teams can receive more telemetry and alerts than they can efficiently investigate. Important signals may be buried among routine events, making prioritization and diagnosis harder.

## Planned capabilities

- Ingest structured, simulated operational events.
- Validate incoming records and handle malformed data.
- Detect unusual behavior using transparent, explainable rules.
- Rank incidents by severity and operational impact.
- Present supporting evidence and a recommended next investigative step.
- Log decisions and errors for debugging and review.
- Include automated tests and reproducible demo scenarios.

## Initial technology

- Python
- pandas
- pytest
- Streamlit for a lightweight operator interface, if useful

## Success criteria

- A new user can run the demo using documented instructions.
- Example events produce repeatable, explainable incident classifications.
- Invalid input is handled gracefully.
- Each incident includes evidence supporting its priority.
- Automated tests cover core classification and error-handling behavior.
- A short screen-recorded demonstration shows the workflow from event ingestion to operator decision.

## Project status

**Planning stage.** The capabilities above are planned, not yet implemented. The system will use simulated data and is not intended for production incident response.

## Future demonstration

The finished demo will show incoming events, highlight an emerging issue, explain why it was prioritized, and guide an operator toward the next investigative action.
