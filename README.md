# Soccer Analytics Capstone Template

## Team

- Thomas LaRock
- Noah Boonin
- Alexander Avramov

## Project
Georgia Tech MSA Spring 2026 – Soccer Analytics Capstone

**Project (Trilemma Foundation): “Delivering Elite European Football (Soccer) Analytics”**

## Project Overview
Build an **MIT-licensed, open-source** pipeline that ingests **public match event data** and produces **interactive player/team analytics dashboards** (e.g., possession chains, xG flow, pressure heatmaps).

> [!IMPORTANT]
> **License Notice**: The code in this repository is licensed under MIT. However, the data sources (StatsBomb and Polymarket) are not covered by the MIT license and have their own licensing terms. See the [Data Licensing](#data-licensing) section below.

## Core Scope
* **Data Processing**: Ingest and version **StatsBomb Open** match event data; **normalize IDs** (team/player/competition); create train/val/test splits.
* **Feature Engineering**: Segment events into **possessions/chains**; derive features like carries, progressive passes, zones of control.
* **Identity Resolution**: Resolve identities across providers (e.g., Transfermarkt/FIFA IDs; handle transfers/loans).
* **Metrics & Analytics**: Compute + store metrics (xG, xThreat, field tilt, packing, PPDA) in DuckDB/Postgres (+ PostGIS optional).
* **Evaluation**: Evaluate vs published benchmarks (e.g., Opta/Understat) and report deviations.
* **Visualization**: Visualize/serve via a **static React + Leaflet** site loading precomputed bundles (filters by match/player/phase/minute range).
* **Performance**: Profile performance (runtime/memory/disk) and document tuning for commodity laptops.

## Market Analysis Integration (Optional)
Analyze market efficiency by correlating match events (xG, momentum) with historical odds and trade volume using **Polymarket** data.

> [!NOTE]
> **Note on Live Data**: We do not provide live price feeds. All Polymarket data is provided as historical Parquet exports for backtesting and analysis.

### Polymarket Data Available
The following data is available in `data/Polymarket/` for analysis:
* `soccer_markets.parquet`: Core metadata for soccer markets (questions, slugs, end dates).
* `soccer_tokens.parquet`: Mapping of markets to specific outcome tokens (e.g., "Yes", "No", team names).
* `soccer_trades.parquet`: Granular, trade-by-trade execution data (price, size, timestamp).
* `soccer_odds_history.parquet`: Time-series odds (price history) reconstructed from order books.
* `soccer_event_stats.parquet`: Aggregated volume and market count per event.
* `soccer_summary.parquet`: High-level market summaries (trade counts, first/last trade).

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

## Getting Started
1. **Fork this repository** to your own GitHub account.
2. **Clone your fork** locally.
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Download the data**:
   ```bash
   python data/download_data.py
   ```
   *Note: This will download both StatsBomb (required) and Polymarket (optional) data.*
5. **Explore the data**:
   Run the EDA template to verify your setup:
   ```bash
   python eda/eda_starter_template.py
   ```

6. **Launch the dashboard**:
   Start the interactive dashboard:
   ```bash
   python template/dashboard_template.py
   ```
   Then open `http://127.0.0.1:8050` in your browser.

   The dashboard features:
   - Dynamic filtering by competition, season, and team
   - Real-time statistics updates
   - Modern dark theme with responsive design
   - Interactive visualizations with searchable filters
   - See `template/dashboard_template.md` for detailed documentation

## Ways of Working / Expectations
* Remote practicum; comms via **Discord**; mentorship and tutorials provided; scope is modular and may evolve.
* **Professionalism + initiative**, comfort with changing specs, **weekly visible progress** (commits), collaboration and respectful conduct.
* **Code open-sourced under MIT** (contributors keep attribution); data licensing is governed by respective providers.


## Data Access
All data for this project can be accessed through this [Google Drive link](https://drive.google.com/drive/folders/1xfY6aRZuB5jbAQ1dcmM7aRLBcQHdBEO0?usp=sharing).

## Data Licensing
This project uses data from multiple sources, each with their own licensing terms:

### StatsBomb Data
- **License**: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) (Creative Commons Attribution-NonCommercial 4.0 International)
- **Usage**: Non-commercial use only, attribution required
- **Citation**: "StatsBomb Open Data"
- **Source**: Publicly available match event data

### Polymarket Data
- **Copyright**: © 2026 Polymarket
- **Usage**: Subject to [Polymarket Terms of Service](https://polymarket.com/terms)
- **Restrictions**: For analytical and research purposes only; users responsible for compliance with local laws and regulations
- **Source**: Historical prediction market data provided through Polymarket APIs

> [!WARNING]
> The data in this project is **not covered by the MIT license**. Users must comply with the licensing terms of each respective data provider when using the data for their own projects or analyses.
