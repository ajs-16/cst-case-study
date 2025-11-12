import datetime
from typing import Any

from dateutil import parser
from pydantic import BaseModel, ConfigDict, Field, field_validator

from fund_analysis.enums import CashflowType, Currency, Side

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

    model_config = ConfigDict(populate_by_name=True)


class ForwardFXTrade(BaseModel):
    trade_date: datetime.date
    delivery_date: datetime.date
    foreign_currency: Currency
    base_currency: Currency
    action: Side
    foreign_notional_amount: float

    @property
    def currency_pair_str(self) -> str:
        return f"{self.foreign_currency.name}/{self.base_currency.name}"

    @property
    def direction(self) -> str:
        other = "BUY" if self.action == Side.SELL else "SELL"
        return (
            f"{self.action.name} {self.foreign_currency.name} / {other} {self.base_currency.name}"
        )

    def to_export_row(self) -> dict[str, Any]:
        return {
            "pair": self.currency_pair_str,
            "trade_date": self.trade_date,
            "delivery_date": self.delivery_date,
            "direction": self.direction,
            "notional_currency": self.foreign_currency.name,
            "notional_amount": self.foreign_notional_amount,
        }
