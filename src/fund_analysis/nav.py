import numpy as np
import pandas as pd

from fund_analysis.enums import Currency


def _calculate_cashflow_net_present_value(
    cashflows: pd.Series, r_annual: float, period_years: float = 0.25
) -> float:
    """
    Calculate the net present value of a series of future cashflows, using:

    NPV = Σ CF(t) / (1 + r) ^ t

    Assumes:
        - The cashflows provided are equally spaced (one period apart)
        - r_annual is the annualised discount rate (from XIRR)
        - period_years is period length in years (0.25 = quarterly)
    """
    if cashflows.size == 0:
        return 0.0

    r_period = (1 + r_annual) ** period_years - 1.0

    cf = np.asarray(cashflows, dtype=float)
    periods = np.arange(0, cashflows.size, dtype=float)

    return float(np.sum(cf / (1.0 + r_period) ** periods))


def build_nav_schedule(
    cashflow_schedule: pd.DataFrame,
    irr_dict: dict[str, float | None],
) -> pd.DataFrame:
    """
    Create a per-currency NAV schedule, where:

    - NAV(t = 0) = 0
    - NAV(t > 0) = NPV of remaining cashflows
    - Discount factor = IRR

    Returns:
        - Dataframe of currency NAV over time.
    """
    nav_df = cashflow_schedule[["date"]].copy()
    n_periods = len(cashflow_schedule)

    for curr in Currency:
        cashflow = cashflow_schedule[curr.name]
        irr = irr_dict[curr.name]
        nav = np.zeros(n_periods, dtype=float)

        if irr is None:
            raise ValueError(f"No IRR for currency: {curr.name}")

        for t in range(1, n_periods):
            nav[t] = _calculate_cashflow_net_present_value(cashflow[t:], irr)

        nav_df[curr.name] = nav

    return nav_df
