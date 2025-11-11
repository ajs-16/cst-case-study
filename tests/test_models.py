import datetime
from typing import Any

from fund_analysis.enums import CashflowType, Currency
from fund_analysis.models import CashflowRecord


def test_cashflow_record_validates_fields(sample_record_dict: dict[str, Any]) -> None:
    record = CashflowRecord.model_validate(sample_record_dict)

    assert record.date == datetime.date(2025, 9, 30)
    assert record.local_currency == Currency.GBP
    assert record.base_currency == Currency.EUR
    assert record.cashflow_type == CashflowType.INVESTMENT
