import datetime

from fund_analysis.enums import CashflowType, Currency
from fund_analysis.models import CashflowRecord


def test_cashflow_record_validates_fields() -> None:
    record = CashflowRecord.model_validate(
        {
            "ID": 1,
            "Fund Name": "Fund I",
            "Date": " 30/09/2025'",
            "Cashflow Type": "Investment",
            "Local Currency": "GPB",
            "Cashflow Amount Local": -100.0,
            "Cashflow Amount Base": -150.0,
            "Base Currency": "EUR",
        }
    )

    assert record.date == datetime.date(2025, 9, 30)
    assert record.local_currency == Currency.GBP
    assert record.base_currency == Currency.EUR
    assert record.cashflow_type == CashflowType.INVESTMENT
