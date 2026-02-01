# Soccer Analytics Exploratory Data Analysis (EDA)

This directory contains tools for performing comprehensive exploratory data analysis on integrated soccer datasets, including prediction market data from Polymarket and tracking/event data from Statsbomb.

## Overview

The analysis script `eda_starter_template.py` provides a structured way to inspect, clean, and summarize the datasets. It includes built-in memory profiling to track resource usage during analysis.

## Architecture

```
eda_starter_template.py (~500 lines)
├── Imports & Constants
├── Memory Tracking (psutil-based)
├── Compact Helpers (header, sub, dist, desc, top)
├── Polymarket Analyzers (6 functions)
├── Statsbomb Analyzers (5 functions)
├── Cross-Dataset Analysis
└── Main Entry Point
```

## Key Analysis Sections

1. **Polymarket Analysis**:
   * **Markets**: Volume stats, status distribution, category breakdown
   * **Tokens**: Outcome distributions and tokens per market
   * **Trades**: Trade size/price statistics, side distribution (Buy/Sell)
   * **Odds History**: Price statistics and snapshot counts
   * **Event Stats**: Aggregated statistics at the event level
   * **Summary**: High-level summary per market

2. **Statsbomb Analysis**:
   * **Matches**: Competition/season distributions and match results
   * **Events**: Event type frequency, shot analysis, pass success rates
   * **Lineups**: Position distributions and card summaries
   * **Three Sixty**: Spatial distribution for 15M+ tracking records
   * **Reference**: Entity type distributions

3. **Cross-Dataset Analysis**:
   * Temporal coverage comparison
   * File size summaries across all datasets

## Utility Functions

Compact helper functions for common operations:

| Function | Purpose |
|----------|---------|
| `header(title)` | Print formatted section header |
| `sub(title)` | Print subsection header |
| `dist(lf, col, n)` | Print value distribution for a column |
| `desc(lf, col)` | Print describe statistics |
| `top(lf, cols, sort_col, n)` | Print top N rows |
| `safe_run(func, name)` | Run analysis with error handling |
| `mem_report()` | Return current/peak memory usage |

## Memory Profiling

The script includes built-in memory tracking using `psutil` to monitor actual process memory (including Polars/Rust allocations):

```
================================================================================
  SOCCER ANALYTICS EDA
================================================================================
Baseline memory: 85.2 MB

[Polymarket complete] Memory: 142.5 MB (peak: 156.3 MB)
[Statsbomb complete] Memory: 198.4 MB (peak: 628.9 MB)

================================================================================
  EDA COMPLETE
================================================================================
Baseline memory: 85.20 MB
Final memory: 198.40 MB
Peak memory: 628.94 MB
Memory used above baseline: 543.74 MB
```

### Memory Usage Breakdown

| Component | Approx. Size |
|-----------|-------------|
| Python + imports | ~80-100 MB |
| Polars runtime | ~50-80 MB |
| Data processing peaks | ~400-500 MB |

Processing ~28 million rows with a peak of ~630 MB demonstrates the efficiency of Polars lazy evaluation. Without it, the same analysis would require 3-5 GB.

## Performance Optimizations

The EDA template is optimized for machines with limited RAM (8GB+) using **Polars**:

* **Lazy Evaluation**: Uses `scan_parquet` to build query plans executed only when collected
* **Column Selection**: Only required columns are loaded
* **Sequential Processing**: Memory released between analysis sections
* **Timestamp Correction**: Handles millisecond/microsecond inconsistencies automatically

## How to Run

Ensure dependencies are installed and data is downloaded:

```bash
pip install -r requirements.txt
python data/download_data.py
```

Then run the EDA:

```bash
python eda/eda_starter_template.py
```

## Programmatic Usage

```python
from eda.eda_starter_template import (
    analyze_pm_markets,
    analyze_sb_matches,
    analyze_sb_events
)

# Run individual analyses
pm_results = analyze_pm_markets()
sb_results = analyze_sb_matches()

# Access summary statistics
print(f"Total markets: {pm_results['total']}")
print(f"Total matches: {sb_results['matches']}")
```

## Requirements

Key dependencies:

* `polars>=0.20.0` - High-performance DataFrame library
* `psutil>=5.9.0` - Memory profiling
* `pyarrow>=14.0.0` - Parquet file support
