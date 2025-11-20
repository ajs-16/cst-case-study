import pandas as pd

from fund_analysis.enums import Currency


def build_cashflow_schedule(
    fund_df: pd.DataFrame,
    date_col: str = "date",
    currency_col: str = "local_currency",
    amount_col: str = "cashflow_amount_local",
) -> pd.DataFrame:
    """
    Convert fund cashflow data into a pivoted dataframe with dates
    as rows and currencies as columns.

    Returns:
        - Dataframe of cashflows per currency.
    """
    cashflow_df = fund_df[[date_col, currency_col, amount_col]].copy()

    cashflows_agg_df = cashflow_df.groupby([currency_col, date_col], as_index=False)[
        amount_col
    ].sum()

    cashflow_pivot_df = (
        cashflows_agg_df.pivot(index=date_col, columns=currency_col, values=amount_col)
        .reindex(columns=[c.name for c in Currency])
        .sort_index()
        .fillna(0.0)
    )

    cashflow_pivot_df.columns.name = None
    cashflow_flat = cashflow_pivot_df.reset_index().rename(columns={date_col: "date"})

    return cashflow_flat
