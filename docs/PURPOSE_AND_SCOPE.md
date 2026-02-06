# Purpose and Scope

## What This Framework Is

This project is a deterministic UI flow exploration framework for test engineering.

It:

- starts from a URL,
- discovers interactable UI elements,
- executes actions and form scenarios,
- classifies outcomes,
- builds a state-transition graph,
- derives test-case candidates,
- stores repeated run history in SQLite.

## What It Is Not

- Not an LLM-driven agent.
- Not a data scraping framework.
- Not a full autonomous testing replacement.

The goal is path discovery and flow observability for automation teams.

## Core Principles

- Deterministic behavior over probabilistic inference.
- Reproducible run artifacts.
- Traceability from UI transitions to generated test cases.
- Historical comparison across repeated runs.

## LLM-Free Guarantee

Runtime execution uses code-only logic:

- Playwright for UI interaction.
- Rule-based discovery and scenario generation.
- Deterministic outcome classification.
- Graph-based test-case derivation.
- SQLite for persistence.

No model/API inference is used during crawling, classification, case generation, or persistence.
