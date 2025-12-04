import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import scrape_data
import pandas as pd


def test_scrape_returns_dataframe():
    """Test that scraping returns a DataFrame"""
    # Test with a simple mock
    result = scrape_data("https://example.com")
    assert isinstance(result, pd.DataFrame)
    assert result is not None


def test_main_module_exists():
    """Test that main module can be imported"""
    import main
    assert hasattr(main, 'scrape_data')
    assert hasattr(main, 'main')


def test_scrape_data_callable():
    """Test that scrape_data is callable"""
    assert callable(scrape_data)
