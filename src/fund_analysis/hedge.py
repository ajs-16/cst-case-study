from datetime import date

import pandas as pd
from dateutil.relativedelta import relativedelta

from fund_analysis.enums import Currency, Side
from fund_analysis.models import ForwardFXTrade


def propose_trades(
    nav_schedule: pd.DataFrame,
    base_currency: Currency,
    months_forward: int = 3,
    use_next_nav_date: bool = False,
) -> list[ForwardFXTrade]:
    """
    Propose £M rolling FX forward contract trades that hedge 100% of non-base NAV exposure.

    - NAV < 0 = long foreign exposure, SELL foregin / BUY base.
    - NAV > 0 = short foreign exposure, BUY foregin / SELL base.
    """
    if nav_schedule.empty:
        return []

    trades: list[ForwardFXTrade] = []

    for idx in range(len(nav_schedule) - 1):
        trade_date: date = nav_schedule.at[idx, "date"]

        if use_next_nav_date:
            delivery_date: date = nav_schedule.at[idx + 1, "date"]
        else:
            delivery_date = trade_date + relativedelta(months=months_forward)

        for currency in Currency:
            if currency == base_currency:
                continue

            nav_value = nav_schedule.at[idx, currency.name]
            action = Side.SELL if nav_value < 0 else Side.BUY

            trade = ForwardFXTrade(
                trade_date=trade_date,
                delivery_date=delivery_date,
                foreign_currency=currency,
                base_currency=base_currency,
                action=action,
                foreign_notional_amount=abs(nav_value),
            )
            trades.append(trade)

    return trades
