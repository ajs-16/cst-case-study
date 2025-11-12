from argparse import ArgumentParser
from pathlib import Path

import pandas as pd

from fund_analysis.hedge import propose_trades
from fund_analysis.io import load_and_validate
from fund_analysis.irr import irr_base, irr_by_currency
from fund_analysis.nav import build_nav_schedule


def setup_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="fund_analysis", description="Fund Analysis CLI: IRR, NAV and hedge trade proposal."
    )

    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        help="Path to Excel input",
        default=Path("data/input/CST_Case_Study_data__1_.xlsx"),
    )

    parser.add_argument("-f", "--fund", help="Fund name filter", default="Fund I")

    parser.add_argument(
        "-o", "--output", type=Path, help="Directory for outputs", default=Path("outputs")
    )

    parser.add_argument("-e", "--export", action="store_true", help="Write results to output files")

    return parser


def main() -> None:
    parser = setup_arg_parser()
    args = parser.parse_args()

    records, df = load_and_validate(args.input)

    df_fund = df[df["fund_name"] == args.fund].copy()
    if df_fund.empty:
        print(f"No cashflow data present in the input file for fund: {args.fund}")
        return

    fund_base_currencies = {
        record.base_currency for record in records if record.fund_name == args.fund
    }
    if len(fund_base_currencies) > 1:
        print(f"Multiple base currencies detected for: {args.fund}: {fund_base_currencies}")
        return

    irr_curr = irr_by_currency(df_fund)
    irr_fund = irr_base(df_fund)

    irr_df = pd.DataFrame(
        [
            {"category": k, "Annualised IRR (XIRR)": (v * 100.0) if v is not None else None}
            for k, v in sorted(irr_curr.items())
        ]
        + [
            {
                "category": f"{args.fund}",
                "Annualised IRR (XIRR)": (irr_fund * 100.0) if irr_fund is not None else None,
            }
        ]
    )

    nav_df = build_nav_schedule(df_fund)

    trades = propose_trades(nav_df, list(fund_base_currencies)[0], use_next_nav_date=True)
    trades_df = pd.DataFrame([t.to_export_row() for t in trades])

    if args.export:
        args.output.mkdir(parents=True, exist_ok=True)
        irr_df.to_csv(args.output / "irr.csv", index=False)
        nav_df.to_csv(args.output / "nav_schedule.csv", index=False)
        trades_df.to_csv(args.output / "hedge_proposals.csv", index=False)

    print(f"Number of records validated: {len(records)}")
    print("\nIRR by currency and fund (%):")
    print(irr_df.to_string(index=False))
    print("\nNAV Schedule preview:")
    print(nav_df.head().to_string(index=False))
    print("\nHedge trade proposals preview:")
    print(trades_df.head().to_string(index=False))


if __name__ == "__main__":
    main()
