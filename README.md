# Soccer Analytics Capstone Template

## Team

- Thomas LaRock
- Noah Boonin
- Alexander Avramov

## Project
Georgia Tech MSA Spring 2026 – Soccer Analytics Capstone

**Project (Trilemma Foundation): “Delivering Elite European Football (Soccer) Analytics”**

## Project Overview
This project aims to build an **MIT-licensed, open-source** pipeline that ingests **public match event data** and produces **interactive player/team analytics dashboards**. The goal is to create actionable insights (e.g., possession chains, xG flow, pressure heatmaps) from raw event data.

> [!IMPORTANT]
> **License Notice**: The code in this repository is licensed under MIT. However, the data sources (StatsBomb and Polymarket) are not covered by the MIT license and have their own licensing terms. See the [Data Licensing](#data-licensing) section below.

## Project Guidelines
This template provides a foundation, but the direction of your analysis is up to you. Below are some areas to focus on as you build your pipeline:

* **Data Processing**: You'll need a way to ingest and version match event data (e.g., StatsBomb). Note that **IDs are currently NOT normalized** across datasets (e.g., StatsBomb team IDs do not currently map to Polymarket market slugs). A critical early task is creating those mapping layers to join betting interest with match events.
* **Feature Engineering**: Consider how to segment the game. breaking matches into **possessions or chains** is a common approach. Think about what derived features (carries, pressure, zones of control) might be predictive or descriptive.
* **Identity Resolution**: Real-world data is messy. You may need to resolve player identities across different providers (e.g., mapping Transfermarkt IDs to match data) or handle player transfers and loans.
* **Metrics & Analytics**: Explore computing standard advanced metrics like **xG, xThreat, or Field Tilt**. Storing these efficiently (e.g., in DuckDB or Postgres) will make analysis much faster.
* **Evaluation**: How do you know your model is good? Consider comparing your meaningful metrics against published benchmarks or using them to identify outliers.
* **Visualization**: Analytics needs to be communicated. A **static React + Leaflet** site is a great way to host interactive visualizations without heavy backend infrastructure.
* **Performance**: Keep an eye on efficiency. Documenting the runtime and memory usage of your pipeline helps ensure it can run on standard hardware.

## Market Analysis Integration (Optional)
Analyze market efficiency by correlating match events (xG, momentum) with historical odds and trade volume using **Polymarket** data. 

> [!TIP]
> **Integration Task**: Since these datasets are from different providers, you'll need to manually resolve entities (e.g., mapping the StatsBomb team name `Arsenal FC` to the Polymarket slug `arsenal`).

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

> [!NOTE]
> **Polymarket timestamps**: `soccer_trades.parquet`, `soccer_odds_history.parquet`, and the `first_trade`/`last_trade` fields in `soccer_summary.parquet` are stored as epoch milliseconds in Parquet `TIMESTAMP` columns. Read them by casting via Int64 -> Datetime(ms) at runtime. The EDA template applies this correction automatically.

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

## Recommended Workflow
* **Communication**: We use **Discord** for day-to-day chat. Feel free to ask questions and share updates there.
* **Progress**: Regular, visible progress (e.g., weekly commits) is the best way to get feedback. We value initiative and the ability to adapt as you learn more about the data.
* **Open Source**: We encourage keeping your code open (MIT License), while respecting the specific licensing terms of the data providers.


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
