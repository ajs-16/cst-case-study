from enum import StrEnum


class CashflowType(StrEnum):
    INVESTMENT = "Investment"
    INTEREST = "Interest"
    PRINCIPAL_REPAYMENT = "Principal Repayment"


class Currency(StrEnum):
    GBP = "GBP"
    EUR = "EUR"
    USD = "USD"


class Side(StrEnum):
    BUY = "Buy"
    SELL = "Sell"
