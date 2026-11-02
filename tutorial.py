from __future__ import annotations

import pandas as pd

INSTANCE_URL = "https://raw.githubusercontent.com/JadeXu16/EPSBench/main/data/instances.csv"
GROUND_TRUTH_URL = "https://raw.githubusercontent.com/JadeXu16/EPSBench/main/data/ground_truth.csv"
PRICES_URL = "https://raw.githubusercontent.com/JadeXu16/EPSBench/main/data/prices.csv"


def load_tables() -> pd.DataFrame:
    instances = pd.read_csv(INSTANCE_URL)
    truth = pd.read_csv(GROUND_TRUTH_URL)
    prices = pd.read_csv(PRICES_URL)

    df = (
        instances.merge(truth, on=["ticker", "fiscal_quarter"], how="inner")
        .merge(prices, on=["ticker", "fiscal_quarter"], how="inner")
        .copy()
    )

    # Keep the column names explicit: the benchmark uses GAAP diluted EPS.
    df = df.rename(columns={"eps_gaap_diluted": "eps_actual"})
    return df


def main() -> None:
    df = load_tables()

    # Two naive baselines the benchmark makes easy to test.
    df["abs_error_last_q"] = (df["eps_last_quarter"] - df["eps_actual"]).abs()
    df["abs_error_yoy"] = (df["eps_year_ago"] - df["eps_actual"]).abs()
    df["pde_last_q"] = df["abs_error_last_q"] / df["close_price"]
    df["pde_yoy"] = df["abs_error_yoy"] / df["close_price"]

    # One concrete wrong-number example from the benchmark.
    example = df[(df["ticker"] == "AMGN") & (df["fiscal_quarter"] == "2025Q4")].iloc[0]

    print("EPSBench audit")
    print("--------------")
    print(f"Rows merged: {len(df)}")
    print()
    print("Concrete wrong-number example:")
    print(
        f"  {example.ticker} {example.fiscal_quarter}: actual EPS={example.eps_actual:.2f}, "
        f"last-quarter EPS={example.eps_last_quarter:.2f}, year-ago EPS={example.eps_year_ago:.2f}, "
        f"close={example.close_price:.4f}"
    )
    print(
        f"  naive last-quarter miss = {example.abs_error_last_q:.2f} EPS points "
        f"(PDE={example.pde_last_q:.4f})"
    )
    print()
    print("Worst naive last-quarter misses in this sample:")
    worst = df.sort_values("abs_error_last_q", ascending=False).head(5)
    cols = ["ticker", "fiscal_quarter", "eps_actual", "eps_last_quarter", "abs_error_last_q", "pde_last_q"]
    print(worst[cols].to_string(index=False, formatters={
        "eps_actual": "{:.2f}".format,
        "eps_last_quarter": "{:.2f}".format,
        "abs_error_last_q": "{:.2f}".format,
        "pde_last_q": "{:.4f}".format,
    }))
    print()
    print("Worst naive year-ago misses in this sample:")
    worst_y = df.sort_values("abs_error_yoy", ascending=False).head(5)
    cols_y = ["ticker", "fiscal_quarter", "eps_actual", "eps_year_ago", "abs_error_yoy", "pde_yoy"]
    print(worst_y[cols_y].to_string(index=False, formatters={
        "eps_actual": "{:.2f}".format,
        "eps_year_ago": "{:.2f}".format,
        "abs_error_yoy": "{:.2f}".format,
        "pde_yoy": "{:.4f}".format,
    }))


if __name__ == "__main__":
    main()
