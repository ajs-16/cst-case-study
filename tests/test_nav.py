from datetime import date

import pandas as pd
import pytest

from fund_analysis.nav import build_nav_schedule


def test_build_nav_schedule(
    cashflow_schedule_df: pd.DataFrame, irr_dict: dict[str, float | None]
) -> None:
    nav_schedule = build_nav_schedule(cashflow_schedule_df, irr_dict)

    assert "date" in nav_schedule.columns
    assert list(nav_schedule["date"]) == [date(2025, 1, 1), date(2026, 1, 1)]

    assert nav_schedule.loc[0, "GBP"] == 0.0
    assert nav_schedule.loc[0, "EUR"] == 0.0
    assert nav_schedule.loc[0, "USD"] == 0.0

    assert nav_schedule.loc[1, "GBP"] > 0
    assert nav_schedule.loc[1, "EUR"] == 0.0
    assert nav_schedule.loc[1, "USD"] > 0


def test_build_nav_schedule_missing_irr(
    cashflow_schedule_df: pd.DataFrame, irr_dict_missing: dict[str, float | None]
) -> None:
    with pytest.raises(ValueError, match="No IRR for currency: GBP"):
        build_nav_schedule(cashflow_schedule_df, irr_dict_missing)
