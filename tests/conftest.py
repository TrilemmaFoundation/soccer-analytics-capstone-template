"""Pytest configuration and shared fixtures for timestamp tests."""
import pytest
from pathlib import Path


def _repo_root() -> Path:
    """Get the repository root directory."""
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def data_dir() -> Path:
    """Return the data directory path."""
    return _repo_root() / "data"


@pytest.fixture
def polymarket_dir(data_dir: Path) -> Path:
    """Return the Polymarket data directory path."""
    return data_dir / "Polymarket"


@pytest.fixture
def statsbomb_dir(data_dir: Path) -> Path:
    """Return the Statsbomb data directory path."""
    return data_dir / "Statsbomb"


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "requires_data: mark test as requiring data files")


@pytest.fixture(autouse=True)
def skip_if_missing_data(request, polymarket_dir: Path):
    """Skip tests that require Polymarket data if files are missing."""
    if request.node.get_closest_marker("requires_data"):
        if not polymarket_dir.exists():
            pytest.skip(f"Polymarket data directory not found: {polymarket_dir}")
