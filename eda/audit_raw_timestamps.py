import math
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


CUTOFF = pd.Timestamp("2020-01-01", tz="UTC")
NAME_HINTS = ("timestamp", "date", "created", "start", "end", "first", "last")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _find_parquet_files(data_dir: Path) -> list[Path]:
    return sorted(data_dir.rglob("*.parquet"))


def _has_name_hint(name: str) -> bool:
    lower = name.lower()
    return any(hint in lower for hint in NAME_HINTS)


def _epoch_unit_from_series(values: pd.Series) -> str | None:
    """Infer epoch unit from magnitude; returns 's' or 'ms'."""
    sample = values.dropna()
    if sample.empty:
        return None
    magnitude = float(sample.iloc[0])
    if math.isnan(magnitude):
        return None
    magnitude = abs(magnitude)
    if magnitude >= 1e12:
        return "ms"
    if magnitude >= 1e9:
        return "s"
    return None


def _normalize_timestamp(series: pd.Series, field: pa.Field) -> pd.Series:
    """Normalize timestamp, detecting ms-as-ns corruption for TIMESTAMP types."""
    if pa.types.is_timestamp(field.type):
        # Check if this looks like ms-as-ns corruption (all values in 1970)
        normalized = pd.to_datetime(series, errors="coerce", utc=True)
        non_null = normalized.dropna()
        if not non_null.empty:
            min_val = non_null.min()
            # If all values are pre-2020, likely ms-as-ns corruption
            if min_val < CUTOFF:
                # Extract raw int64 and reinterpret as milliseconds
                raw_int = normalized.astype("int64")
                raw_int = raw_int[raw_int != pd.NaT.value]
                if not raw_int.empty:
                    # Reinterpret as milliseconds
                    corrected = pd.to_datetime(raw_int, unit="ms", errors="coerce", utc=True)
                    # Verify correction produces plausible dates
                    if not corrected.isna().all() and corrected.min() >= CUTOFF:
                        return corrected
        return normalized

    if pa.types.is_integer(field.type) and _has_name_hint(field.name):
        unit = _epoch_unit_from_series(series)
        if unit is None:
            return pd.to_datetime(series, errors="coerce", utc=True)
        return pd.to_datetime(series, errors="coerce", unit=unit, utc=True)

    if pa.types.is_string(field.type) and _has_name_hint(field.name):
        return pd.to_datetime(series, errors="coerce", utc=True)

    return pd.to_datetime(series, errors="coerce", utc=True)


def _timestamp_fields(schema: pa.Schema) -> list[pa.Field]:
    fields = []
    for field in schema:
        if pa.types.is_timestamp(field.type):
            fields.append(field)
        elif (pa.types.is_integer(field.type) or pa.types.is_string(field.type)) and _has_name_hint(
            field.name
        ):
            fields.append(field)
    return fields


def _range_from_raw(raw_int: pd.Series, unit: str) -> tuple[pd.Timestamp, pd.Timestamp]:
    if raw_int.empty:
        return pd.NaT, pd.NaT
    converted = pd.to_datetime(raw_int, unit=unit, errors="coerce", utc=True)
    if converted.isna().all():
        return pd.NaT, pd.NaT
    return converted.min(), converted.max()


def audit_file(path: Path) -> list[dict]:
    parquet_file = pq.ParquetFile(path)
    schema = parquet_file.schema_arrow
    fields = _timestamp_fields(schema)

    if not fields:
        print(f"{path.name}: no timestamp-like columns found.")
        return []

    columns = [field.name for field in fields]
    table = pq.read_table(path, columns=columns)
    df = table.to_pandas()

    results = []
    for field in fields:
        # Get raw values before normalization for diagnosis
        raw_series = df[field.name]
        series = _normalize_timestamp(raw_series, field)
        total = int(series.size)
        nulls = int(series.isna().sum())
        pre_2020 = int((series < CUTOFF).sum())
        min_value = series.min()
        max_value = series.max()
        
        # Diagnosis: determine if corruption was detected and fixed
        diagnosis = "OK"
        alt_ms_min = pd.NaT
        alt_ms_max = pd.NaT
        if pre_2020 > 0 and pa.types.is_timestamp(field.type):
            # Check if ms-as-ns corruption exists
            raw_dt = pd.to_datetime(raw_series, errors="coerce", utc=True)
            raw_int = raw_dt.astype("int64")
            raw_int = raw_int[raw_int != pd.NaT.value]
            if not raw_int.empty:
                alt_ms_min, alt_ms_max = _range_from_raw(raw_int, "ms")
                if not pd.isna(alt_ms_min) and alt_ms_min >= CUTOFF:
                    diagnosis = "CORRUPTED (ms-as-ns, fix: cast Int64->Datetime(ms))"
                else:
                    diagnosis = "CORRUPTED (unknown cause)"
        elif pre_2020 > 0:
            diagnosis = "CORRUPTED (pre-2020 values)"
        
        results.append(
            {
                "file": path.name,
                "column": field.name,
                "total": total,
                "nulls": nulls,
                "pre_2020": pre_2020,
                "min": min_value,
                "max": max_value,
                "diagnosis": diagnosis,
                "alt_ms_min": alt_ms_min,
                "alt_ms_max": alt_ms_max,
            }
        )

    return results


def main() -> None:
    data_dir = _repo_root() / "data" / "Polymarket"
    if not data_dir.exists():
        print(f"Missing data directory: {data_dir}")
        print("Run `python data/download_data.py` first.")
        return

    parquet_files = _find_parquet_files(data_dir)
    if not parquet_files:
        print(f"No parquet files found in {data_dir}")
        return

    all_results = []
    for path in parquet_files:
        all_results.extend(audit_file(path))

    if not all_results:
        return

    results_df = pd.DataFrame(all_results)
    suspicious = results_df[results_df["pre_2020"] > 0].copy()

    print("\n=== Timestamp Audit Summary ===")
    base_cols = ["file", "column", "total", "nulls", "pre_2020", "min", "max", "diagnosis"]
    print(results_df.sort_values(["file", "column"])[base_cols].to_string(index=False))

    if suspicious.empty:
        print("\nNo pre-2020 timestamps detected.")
    else:
        print("\n=== Potentially Corrupted (pre-2020) ===")
        alt_cols = ["alt_ms_min", "alt_ms_max"]
        cols = base_cols + alt_cols
        print(suspicious.sort_values(["file", "column"])[cols].to_string(index=False))


if __name__ == "__main__":
    main()
