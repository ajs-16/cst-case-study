# Fund Analysis - CST Case Study

This repository contains my solution to the **CST Case Study**. The program reads cashflow data, validates it with Pydantic models and performs three analysis tasks:

1. **Internal Rate of Return (IRR)** - at both currency and fund level.
2. **Net Asset Value (NAV) Schedule** - Cumulative cashflows per currency.
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
    pip install -e "." # Runtime dependencies only
    pip install -e ".[dev]" # Runtime and development dependencies
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
