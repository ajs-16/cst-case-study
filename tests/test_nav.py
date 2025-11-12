import pandas as pd

from fund_analysis.nav import build_nav_schedule


def test_build_nav_schedule(multi_currency_cashflow_df: pd.DataFrame) -> None:
    nav_schedule = build_nav_schedule(multi_currency_cashflow_df)

    assert nav_schedule.loc[0, "GBP"] == -1000.0
    assert nav_schedule.loc[0, "EUR"] == 0.0
    assert nav_schedule.loc[0, "USD"] == -1000.0

    assert nav_schedule.loc[1, "GBP"] == 95.0
    assert nav_schedule.loc[1, "EUR"] == 0.0
    assert nav_schedule.loc[1, "USD"] == 120.0
