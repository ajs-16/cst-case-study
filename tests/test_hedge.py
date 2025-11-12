from datetime import date

import pandas as pd

from fund_analysis.enums import Currency, Side
from fund_analysis.hedge import propose_trades


def test_propose_trades(sample_nav_df: pd.DataFrame) -> None:
    trades = propose_trades(sample_nav_df, Currency.EUR, use_next_nav_date=True)

    assert len(trades) == 4

    t0 = trades[0]
    assert t0.currency_pair_str == "GBP/EUR"
    assert t0.action == Side.SELL
    assert t0.foreign_notional_amount == 100.0
    assert t0.delivery_date == date(2025, 12, 31)
