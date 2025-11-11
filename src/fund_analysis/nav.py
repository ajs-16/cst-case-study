import pandas as pd

from fund_analysis.enums import Currency


def build_nav_schedule(
    df: pd.DataFrame,
    date_col: str = "date",
    currency_col: str = "local_currency",
    amount_col: str = "cashflow_amount_local",
) -> pd.DataFrame:
    """
    Create a per-currency NAV over time.

    Returns:
        - Dataframe of currency NAV over time.
    """

    cashflow_df = df[[date_col, currency_col, amount_col]].copy()

    cashflows_agg_df = cashflow_df.groupby([currency_col, date_col], as_index=False)[
        amount_col
    ].sum()

    cashflow_pivot_df = (
        cashflows_agg_df.pivot(index=date_col, columns=currency_col, values=amount_col)
        .reindex(columns=[c.name for c in Currency])
        .sort_index()
        .fillna(0.0)
    )
    nav_df = cashflow_pivot_df.cumsum()

    nav_df.columns.name = None
    nav_flat = nav_df.reset_index().rename(columns={date_col: "date"})

    return nav_flat
