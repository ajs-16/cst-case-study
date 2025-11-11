import pandas as pd

from fund_analysis.irr import calculate_irr, irr_by_currency


def test_calculate_irr_single(simple_cashflow_df: pd.DataFrame) -> None:
    irr = calculate_irr(simple_cashflow_df)
    assert irr is not None
    assert 0.095 < irr < 0.105


def test_calculate_currency(multi_currency_cashflow_df: pd.DataFrame) -> None:
    curr_irr = irr_by_currency(multi_currency_cashflow_df)
    assert curr_irr["GBP"] is not None
    assert curr_irr["USD"] is not None
