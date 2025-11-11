from pathlib import Path
from typing import Any

import pandas as pd

from fund_analysis.enums import Currency
from fund_analysis.io import load_and_validate
from fund_analysis.models import CashflowRecord


def test_load_and_validate_success(
    tmp_path: Path, sample_record_dict: dict[str, Any], clean_record_dict: dict[str, Any]
) -> None:
    df = pd.DataFrame([sample_record_dict, clean_record_dict])
    tmp_xlsx = tmp_path / "records.xlsx"
    df.to_excel(tmp_xlsx, index=False)

    records, df_validated = load_and_validate(tmp_xlsx)

    assert len(records) == 2
    assert all(isinstance(record, CashflowRecord) for record in records)
    assert df_validated.loc[0, "local_currency"] == Currency.GBP
