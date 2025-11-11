import datetime

from pydantic import BaseModel, Field

from fund_analysis.enums import CashflowType, Currency


class CashflowRecord(BaseModel):
    """
    Represents a single cashflow record for a fund.
    """

    id: int = Field(alias="ID")
    fund_name: str = Field(alias="Fund Name")
    date: datetime.date = Field(alias="Date")
    cashflow_type: CashflowType = Field(alias="Cashflow Type")
    local_currency: Currency = Field(alias="Local Currency")
    cashflow_amount_local: float = Field(alias="Cashflow Amount Local")
    cashflow_amount_base: float = Field(alias="Cashflow Amount Base")
    base_currency: Currency = Field(alias="Base Currency")

    class Config:
        populate_by_name = True
