import datetime
from typing import Any

from dateutil import parser
from pydantic import BaseModel, Field, field_validator

from fund_analysis.enums import CashflowType, Currency

CURRENCY_TYPO_MAP = {"GPB": "GBP"}


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

    @field_validator("local_currency", "base_currency", mode="before")
    def correct_currency_typos(cls, v: Any) -> Any:
        if v in CURRENCY_TYPO_MAP:
            return CURRENCY_TYPO_MAP[v]
        return v

    @field_validator("date", mode="before")
    def clean_dates(cls, v: Any) -> Any:
        if isinstance(v, str):
            clean = v.strip().replace("`", "")
            return parser.parse(clean, dayfirst=True)
        return v

    class Config:
        populate_by_name = True
