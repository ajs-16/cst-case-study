from pathlib import Path
from typing import List, Tuple

import pandas as pd

from fund_analysis.models import CashflowRecord


def load_and_validate(data_path: Path | str) -> Tuple[List[CashflowRecord], pd.DataFrame]:
    """
    Reads fund cashflow data from xlsx file and validates each record using
    the CashflowRecord model.

    Returns:
        - records: List[CashflowRecord] (validated objects)
        - df: pd.DataFrame of validated records

    Notes:
        - Assumes column headers match the Field aliases defined in CashflowRecord.
        - Relies on CashflowRecord validators for cleaning input data.
    """

    raw_df = pd.read_excel(data_path, engine="openpyxl")
    raw_records = raw_df.to_dict(orient="records")

    validated_records = [CashflowRecord.model_validate(record) for record in raw_records]
    df = pd.DataFrame([record.model_dump() for record in validated_records])

    return (validated_records, df)
