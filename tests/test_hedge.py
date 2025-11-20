from datetime import date

import pandas as pd

from fund_analysis.enums import Currency, Side
from fund_analysis.hedge import propose_trades


def test_propose_trades() -> None:
    nav_schedule = pd.DataFrame(
        {
            "date": [date(2025, 9, 30), date(2025, 12, 31), date(2026, 3, 31)],
            "GBP": [0.0, 100.0, 90.0],
            "EUR": [0.0, 150.0, 140.0],
            "USD": [0.0, 200.0, 190.0],
        }
    )

    cashflow_schedule = pd.DataFrame(
        {
            "date": [date(2025, 9, 30), date(2025, 12, 31), date(2026, 3, 31)],
            "GBP": [-100.0, 10.0, 5.0],
            "EUR": [-150.0, 10.0, 5.0],
            "USD": [-200.0, 10.0, 5.0],
        }
    )
    trades = propose_trades(nav_schedule, cashflow_schedule, Currency.EUR, use_next_nav_date=True)

    assert len(trades) == 2

    gbp_trades = [trade for trade in trades if trade.foreign_currency == Currency.GBP]

    assert len(gbp_trades) == 1

    gbp_trade = gbp_trades[0]
    assert gbp_trade.currency_pair_str == "GBP/EUR"
    assert gbp_trade.action == Side.SELL
    assert gbp_trade.foreign_notional_amount == 90.0
    assert gbp_trade.delivery_date == date(2026, 3, 31)
