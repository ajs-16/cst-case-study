from datetime import date
from typing import Any

import pandas as pd
import pytest

from fund_analysis.enums import Currency


@pytest.fixture
def sample_record_dict() -> dict[str, Any]:
    """A cashflow record dict with formatting issus to test cleaning."""

    return {
        "ID": 1,
        "Fund Name": "Fund I",
        "Date": " 30/09/2025'",
        "Cashflow Type": "Investment",
        "Local Currency": "GPB",
        "Cashflow Amount Local": -100.0,
        "Cashflow Amount Base": -150.0,
        "Base Currency": "EUR",
    }


@pytest.fixture
def clean_record_dict() -> dict[str, Any]:
    """A valid and clean sample cashflow record for testing"""

    return {
        "ID": 2,
        "Fund Name": "Fund I",
        "Date": "30/09/2025",
        "Cashflow Type": "Interest",
        "Local Currency": "GBP",
        "Cashflow Amount Local": 10.0,
        "Cashflow Amount Base": 15,
        "Base Currency": "EUR",
    }


@pytest.fixture
def simple_cashflow_df() -> pd.DataFrame:
    """Simple cashflow schedule."""
    return pd.DataFrame(
        {"date": [date(2025, 1, 1), date(2026, 1, 1)], "cashflow_amount": [-1000.0, 1100.0]}
    )


@pytest.fixture
def multi_currency_cashflow_df() -> pd.DataFrame:
    """Multi-currency cashflow schedule."""
    return pd.DataFrame(
        {
            "date": [date(2025, 1, 1), date(2026, 1, 1), date(2025, 1, 1), date(2026, 1, 1)],
            "local_currency": [Currency.GBP, Currency.GBP, Currency.USD, Currency.USD],
            "cashflow_amount_local": [-1000.0, 1095.0, -1000.0, 1120.0],
        }
    )


@pytest.fixture
def sample_nav_df() -> pd.DataFrame:
    """Simple NAV schedule for testing."""
    return pd.DataFrame(
        {
            "date": [date(2025, 9, 30), date(2025, 12, 31), date(2026, 3, 31)],
            "GBP": [-100.0, -90.0, 10.0],
            "EUR": [-150.0, -140.0, 50.0],
            "USD": [-200.0, -190.0, 100.0],
        }
    )


@pytest.fixture
def irr_dict() -> dict[str, float | None]:
    """Sample IRR dictionary."""
    return {
        "GBP": 0.095,
        "EUR": 0.1,
        "USD": 0.12,
    }


@pytest.fixture
def irr_dict_missing() -> dict[str, float | None]:
    """Sample IRR dictionary with missing value."""
    return {
        "GBP": None,
        "EUR": 0.1,
        "USD": 0.12,
    }


@pytest.fixture
def cashflow_schedule_df() -> pd.DataFrame:
    """Sample cashflow schedule (output of build_cashflow_schedule)."""
    return pd.DataFrame(
        {
            "date": [date(2025, 1, 1), date(2026, 1, 1)],
            "GBP": [-1000.0, 1095.0],
            "EUR": [0.0, 0.0],
            "USD": [-1000.0, 1120.0],
        }
    )
