# Soccer Analytics Capstone Template

**Project (Trilemma Foundation): “Delivering Elite European Football (Soccer) Analytics”**

## Project Overview
Build an **MIT-licensed, open-source** pipeline that ingests **public match event data** and produces **interactive player/team analytics dashboards** (e.g., possession chains, xG flow, pressure heatmaps).

## Core Scope
* **Ingest + version** StatsBomb Open + other public sources; **normalize IDs** (team/player/competition); create train/val/test splits.
* **Segment** events into **possessions/chains**; derive features like carries, progressive passes, zones of control.
* **Identity resolution** across providers (e.g., Transfermarkt/FIFA IDs; handle transfers/loans).
* **Compute + store metrics** (xG, xThreat, field tilt, packing, PPDA) in DuckDB/Postgres (+ PostGIS optional).
* **Evaluate** vs published benchmarks (e.g., Opta/Understat) and report deviations.
* **Visualize/serve** via a **static React + Leaflet** site loading precomputed bundles (filters by match/player/phase/minute range).
* **Profile performance** (runtime/memory/disk) and document tuning for commodity laptops.

## Stretch Goals (Optional)
* Nightly incremental updater
* Transformer sequence classifier for press events
* Role embeddings
* xG calibration curves
* CLI export of media-ready heatmaps

## Expected Deliverables
* Public **MIT GitHub repo** (core “product”).
* **Static dashboard** (local render + redeploy on updates) and a **dynamic/on-demand** dashboard for latest/user-specified matches.
* Strong **docs** (README, setup, usage) + **educational notebooks**.
* Optional **public-facing clips/shorts** demonstrating insights.

## Ways of Working / Expectations
* Remote practicum; comms via **Discord**; mentorship and tutorials provided; scope is modular and may evolve.
* **Professionalism + initiative**, comfort with changing specs, **weekly visible progress** (commits), collaboration and respectful conduct.
* **All IP open-sourced under MIT** (contributors keep attribution).

## Capstone (ST498/LSE) Expectations
* **Mandatory milestones/deliverables**: 1st presentation (objectives + plan), 2nd presentation (update + partial results), **draft report**, **final group + individual reports**.
* **Student responsibilities**: project management + work plan, clear individual contributions, proactive unblocking (data/APIs/compute), report writing/presentations.
* **Confidentiality/NDAs**: do not disclose project info externally without partner authorization (incl. social/media/CV) if NDA/onboarding applies.
* **Generative AI**: allowed, but must align with supervisor/partner guidance and be **acknowledged** in outputs.

## Data Access
All data for this project can be accessed through this [Google Drive link](https://drive.google.com/drive/folders/1xfY6aRZuB5jbAQ1dcmM7aRLBcQHdBEO0?usp=sharing).
