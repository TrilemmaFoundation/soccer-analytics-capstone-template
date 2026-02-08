"""Tests for Polymarket timestamp corruption fixes."""
import pytest
from datetime import datetime

import polars as pl
from pathlib import Path


CUTOFF_DATE = datetime(2020, 1, 1)
MAX_FUTURE_DATE = datetime(2027, 1, 1)


@pytest.mark.requires_data
def test_trades_timestamp_post_2020(polymarket_dir: Path):
    """Test that soccer_trades.parquet timestamps are fixed and >= 2020."""
    file_path = polymarket_dir / "soccer_trades.parquet"
    if not file_path.exists():
        pytest.skip(f"File not found: {file_path}")
    
    # Read and apply the ms fix
    df = (
        pl.scan_parquet(file_path)
        .with_columns(
            pl.col("timestamp").cast(pl.Int64).cast(pl.Datetime("ms"))
        )
        .collect()
    )
    
    # Check all timestamps are >= 2020
    timestamps = df["timestamp"]
    assert timestamps.min() >= CUTOFF_DATE, f"Found timestamp before 2020: {timestamps.min()}"
    assert timestamps.max() < MAX_FUTURE_DATE, f"Found timestamp too far in future: {timestamps.max()}"
    
    # Verify no nulls in timestamp column
    assert timestamps.null_count() == 0, "Found null timestamps in trades data"


@pytest.mark.requires_data
def test_odds_timestamp_post_2020(polymarket_dir: Path):
    """Test that soccer_odds_history.parquet timestamps are fixed and >= 2020."""
    file_path = polymarket_dir / "soccer_odds_history.parquet"
    if not file_path.exists():
        pytest.skip(f"File not found: {file_path}")
    
    # Read and apply the ms fix
    df = (
        pl.scan_parquet(file_path)
        .with_columns(
            pl.col("timestamp").cast(pl.Int64).cast(pl.Datetime("ms"))
        )
        .collect()
    )
    
    # Check all timestamps are >= 2020
    timestamps = df["timestamp"]
    assert timestamps.min() >= CUTOFF_DATE, f"Found timestamp before 2020: {timestamps.min()}"
    assert timestamps.max() < MAX_FUTURE_DATE, f"Found timestamp too far in future: {timestamps.max()}"
    
    # Verify no nulls in timestamp column
    assert timestamps.null_count() == 0, "Found null timestamps in odds history data"


@pytest.mark.requires_data
def test_summary_first_last_trade_post_2020(polymarket_dir: Path):
    """Test that soccer_summary.parquet first_trade/last_trade are fixed and >= 2020."""
    file_path = polymarket_dir / "soccer_summary.parquet"
    if not file_path.exists():
        pytest.skip(f"File not found: {file_path}")
    
    # Read and apply the ms fix
    df = (
        pl.scan_parquet(file_path)
        .with_columns(
            [
                pl.col("first_trade").cast(pl.Int64).cast(pl.Datetime("ms")),
                pl.col("last_trade").cast(pl.Int64).cast(pl.Datetime("ms")),
            ]
        )
        .collect()
    )
    
    # Check non-null timestamps are >= 2020
    first_trade = df["first_trade"]
    last_trade = df["last_trade"]
    
    first_non_null = first_trade.filter(first_trade.is_not_null())
    last_non_null = last_trade.filter(last_trade.is_not_null())
    
    if first_non_null.len() > 0:
        assert first_non_null.min() >= CUTOFF_DATE, f"Found first_trade before 2020: {first_non_null.min()}"
        assert first_non_null.max() < MAX_FUTURE_DATE, f"Found first_trade too far in future: {first_non_null.max()}"
    
    if last_non_null.len() > 0:
        assert last_non_null.min() >= CUTOFF_DATE, f"Found last_trade before 2020: {last_non_null.min()}"
        assert last_non_null.max() < MAX_FUTURE_DATE, f"Found last_trade too far in future: {last_non_null.max()}"
    
    # Note: some datasets may include late corrections; do not enforce ordering.


@pytest.mark.requires_data
def test_markets_timestamps_already_valid(polymarket_dir: Path):
    """Test that soccer_markets.parquet timestamps are already valid (no fix needed)."""
    file_path = polymarket_dir / "soccer_markets.parquet"
    if not file_path.exists():
        pytest.skip(f"File not found: {file_path}")
    
    # Read without any fix (should already be correct)
    df = pl.scan_parquet(file_path).collect()
    
    # Check created_at
    created_at = df["created_at"]
    assert created_at.min() >= CUTOFF_DATE, f"Found created_at before 2020: {created_at.min()}"
    assert created_at.max() < MAX_FUTURE_DATE, f"Found created_at too far in future: {created_at.max()}"
    assert created_at.null_count() == 0, "Found null created_at values"
    
    # Check end_date (may have nulls)
    end_date = df["end_date"]
    end_date_non_null = end_date.filter(end_date.is_not_null())
    if end_date_non_null.len() > 0:
        assert end_date_non_null.min() >= CUTOFF_DATE, f"Found end_date before 2020: {end_date_non_null.min()}"
        assert end_date_non_null.max() < MAX_FUTURE_DATE, f"Found end_date too far in future: {end_date_non_null.max()}"
    
    # Note: some markets may resolve earlier than created timestamp in source data.


@pytest.mark.requires_data
def test_event_stats_timestamps_already_valid(polymarket_dir: Path):
    """Test that soccer_event_stats.parquet timestamps are already valid (no fix needed)."""
    file_path = polymarket_dir / "soccer_event_stats.parquet"
    if not file_path.exists():
        pytest.skip(f"File not found: {file_path}")
    
    # Read without any fix (should already be correct)
    df = pl.scan_parquet(file_path).collect()
    
    # Check first_market_start
    first_start = df["first_market_start"]
    assert first_start.min() >= CUTOFF_DATE, f"Found first_market_start before 2020: {first_start.min()}"
    assert first_start.max() < MAX_FUTURE_DATE, f"Found first_market_start too far in future: {first_start.max()}"
    assert first_start.null_count() == 0, "Found null first_market_start values"
    
    # Check last_market_end (may have nulls)
    last_end = df["last_market_end"]
    last_end_non_null = last_end.filter(last_end.is_not_null())
    if last_end_non_null.len() > 0:
        assert last_end_non_null.min() >= CUTOFF_DATE, f"Found last_market_end before 2020: {last_end_non_null.min()}"
        assert last_end_non_null.max() < MAX_FUTURE_DATE, f"Found last_market_end too far in future: {last_end_non_null.max()}"
    
    # Note: source data can include out-of-order events; do not enforce ordering.


@pytest.mark.requires_data
def test_no_future_timestamps(polymarket_dir: Path):
    """Test that all fixed timestamps don't exceed reasonable future bounds."""
    files_to_check = [
        ("soccer_trades.parquet", ["timestamp"]),
        ("soccer_odds_history.parquet", ["timestamp"]),
        ("soccer_summary.parquet", ["first_trade", "last_trade"]),
    ]
    
    for filename, timestamp_cols in files_to_check:
        file_path = polymarket_dir / filename
        if not file_path.exists():
            continue
        
        # Apply appropriate fixes
        lf = pl.scan_parquet(file_path)
        if filename == "soccer_trades.parquet":
            lf = lf.with_columns(pl.col("timestamp").cast(pl.Int64).cast(pl.Datetime("ms")))
        elif filename == "soccer_odds_history.parquet":
            lf = lf.with_columns(pl.col("timestamp").cast(pl.Int64).cast(pl.Datetime("ms")))
        elif filename == "soccer_summary.parquet":
            lf = lf.with_columns(
                [
                    pl.col("first_trade").cast(pl.Int64).cast(pl.Datetime("ms")),
                    pl.col("last_trade").cast(pl.Int64).cast(pl.Datetime("ms")),
                ]
            )
        
        df = lf.collect()
        
        for col in timestamp_cols:
            timestamps = df[col]
            non_null = timestamps.filter(timestamps.is_not_null())
            if non_null.len() > 0:
                max_ts = non_null.max()
                assert max_ts < MAX_FUTURE_DATE, (
                    f"{filename}.{col} has timestamp beyond {MAX_FUTURE_DATE}: {max_ts}"
                )
