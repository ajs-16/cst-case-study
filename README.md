# Fund Analysis - CST Case Study

This repository contains my solution to the **CST Case Study**. The program reads cashflow data, validates it with Pydantic models and performs three analyses:

1. **Internal Rate of Return (IRR)** - at both currency and fund level.
2. **Net Asset Value (NAV) Schedule** - cumulative cashflows per currency.
3. **FX Hedge Proposals** - generates suggested 3-month rolling FX forward contracts to hedge 100% of foreign NAV exposure.

## Requirements

-   Python >= 3.12
-   Dependencies managed via `pyproject.toml`

## Installation

1. Create + activate venv:

    ```bash
    python -m venv .venv
    ```

2. Install package

    ```bash
    pip install . # Runtime dependencies only
    pip install ".[dev]" # Runtime and development dependencies
    pip install -e ".[dev]" # Editable install for development
    ```

## Usage

Run analysis via the CLI:

```bash
python -m fund_analysis.cli --help
```

### CLI Options

| Flag         | Description                    | Default                                   |
| ------------ | ------------------------------ | ----------------------------------------- |
| -i, --input  | Path to xlsx input file        | data/input/CST*Case_Study_data\_\_1*.xlsx |
| -f, --fund   | Fund name filter               | Fund I                                    |
| -o, --output | Output directory               | outputs/                                  |
| -e, --export | Export results to output files | off                                       |

## Methodology

### IRR Calculation

Internal Rate of Return is calculated using XIRR.

-   Handles irregular cashflow timing by using exact dates
-   Calculated separately for each currency
-   Fund level IRR calculated using base currency cashflows

### NAV Calculation

The NAV schedule is calculated as the present value of remaining cashflows at each time(t).

-   NAV(0) = 0 (as specified in the requirements)
-   Cashflows at time t are included in NAV(t)
-   Discount rate = The period IRR which is calculated from the annualised XIRR

### FX Risk Hedging

```
NAV Exposure(t) = NAV(t) - Cashflow(t)
```

**Reasoning**: Cashflows occuring at time t are converted to base currency, so should be excluded from the hedge.

**Direction**:

-   **Positive NAV Exposure** (long foreign currency) = SELL FOREIGN / BUY BASE
-   **Negative NAV Exposure** (short foreign currency) = BUY FOREIGN / SELL BASE

**Implementation details**:

-   Hedging starts at t=1 and finishes at t=n-1
-   100% hedge ratio applied to NAV exposure

## Results / Example Outputs

Pre-generated results can be found in:

```
examples/outputs/
- irr.csv
- nav_schedule.csv
- hedge_proposals.csv
```

## Testing

Pytest testing framework is used to write and manage tests.

Run tests:

```bash
pytest .
```

**NOTE**: Requires fund_analysis package + dev dependencies installed in environment, see [installation](#installation)

## Development & Tooling

-   **Formatting:** Black
-   **Linting:** ruff
-   **Type Checking:** mypy
-   **Testing:** pytest

Pre-commit is used to auto-run all of the above tools before each commit.

To install pre-commit hooks:

```bash
pre-commit install
```
