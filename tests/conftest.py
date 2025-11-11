from typing import Any

import pytest


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
