import pandas as pd
from pyxirr import is_conventional_cash_flow, xirr

from fund_analysis.enums import Currency


def calculate_irr(
    df: pd.DataFrame, date_col: str = "date", amount_col: str = "cashflow_amount"
) -> float | None:
    """
    Calculate the IRR for a single series of dated cashflows.

    Returns:
        - IRR: float
    """
    if df.empty:
        return None

    cashflow_series = df[[date_col, amount_col]].copy().sort_values(date_col)

    if not is_conventional_cash_flow(cashflow_series[amount_col]):
        raise ValueError("Non-conventional cashflow")

    irr: float | None = xirr(cashflow_series[date_col], cashflow_series[amount_col])

    return irr


def irr_by_currency(
    df: pd.DataFrame,
    date_col: str = "date",
    amount_col: str = "cashflow_amount_local",
    currency_col: str = "local_currency",
) -> dict[str, float | None]:
    """
    Calculate the IRR for each local currency.

    Returns:
        - Dict of currency names and their associated IRR.
    """
    curr_irr: dict[str, float | None] = {}

    for curr in Currency:
        cur_df = df.loc[df[currency_col] == curr, [date_col, amount_col]]
        curr_irr[curr.name] = calculate_irr(cur_df, date_col=date_col, amount_col=amount_col)

    return curr_irr


def irr_base(
    df: pd.DataFrame, date_col: str = "date", amount_col: str = "cashflow_amount_base"
) -> float | None:
    """
    Calculate fund level IRR using base-currency cashflows.
    """
    return calculate_irr(df, date_col=date_col, amount_col=amount_col)
