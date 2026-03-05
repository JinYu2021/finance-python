from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

import pandas as pd


REQUIRED_COLUMNS: Dict[str, str] = {
    "project": "Project",
    "period": "Period",
    "revenue": "Revenue",
    "operatingcost": "OperatingCost",
    "capex": "Capex",
    "tax": "Tax",
    "workingcapitaldelta": "WorkingCapitalDelta",
}


def normalize_key(name: str) -> str:
    return "".join(ch for ch in name if ch.isalnum()).lower()


def normalize_and_validate_columns(df: pd.DataFrame) -> pd.DataFrame:
    normalized_to_original = {normalize_key(col): col for col in df.columns}

    missing = [k for k in REQUIRED_COLUMNS if k not in normalized_to_original]
    if missing:
        required_names = ", ".join(REQUIRED_COLUMNS.values())
        raise ValueError(
            f"Excel 缺少必要列: {missing}。请提供列: {required_names}"
        )

    rename_map = {
        normalized_to_original[k]: REQUIRED_COLUMNS[k]
        for k in REQUIRED_COLUMNS
    }
    return df.rename(columns=rename_map)


def load_input_excel(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"未找到输入文件: {path}")

    df = pd.read_excel(path)
    if df.empty:
        raise ValueError("输入 Excel 为空")

    df = normalize_and_validate_columns(df)

    df["Period"] = pd.to_datetime(df["Period"], errors="coerce")
    if df["Period"].isna().any():
        raise ValueError("Period 列包含无法解析的日期")

    numeric_cols = [
        "Revenue",
        "OperatingCost",
        "Capex",
        "Tax",
        "WorkingCapitalDelta",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if df[col].isna().any():
            raise ValueError(f"{col} 列包含非数值内容")

    df = df.sort_values(["Project", "Period"]).reset_index(drop=True)
    return df


def calculate_actual_cashflow(df: pd.DataFrame) -> pd.DataFrame:
    actual = df.copy()
    actual["NetCashFlow"] = (
        actual["Revenue"]
        - actual["OperatingCost"]
        - actual["Capex"]
        - actual["Tax"]
        - actual["WorkingCapitalDelta"]
    )
    actual["CumulativeCashFlow"] = actual.groupby("Project")["NetCashFlow"].cumsum()
    actual["Scenario"] = "Actual"
    return actual


def mean_growth_rate(series: pd.Series) -> float:
    changes = series.pct_change().replace([float("inf"), -float("inf")], pd.NA).dropna()
    if changes.empty:
        return 0.0
    return float(changes.mean())


def forecast_one_project(project_df: pd.DataFrame, forecast_periods: int) -> pd.DataFrame:
    ordered = project_df.sort_values("Period").copy()
    project_name = ordered["Project"].iloc[0]

    rev_growth = mean_growth_rate(ordered["Revenue"])
    cost_growth = mean_growth_rate(ordered["OperatingCost"])

    capex_base = float(ordered["Capex"].tail(3).mean())
    tax_base = float(ordered["Tax"].tail(3).mean())
    wc_base = float(ordered["WorkingCapitalDelta"].tail(3).mean())

    prev_period = ordered["Period"].iloc[-1]
    prev_revenue = float(ordered["Revenue"].iloc[-1])
    prev_cost = float(ordered["OperatingCost"].iloc[-1])
    cumulative = float(ordered["CumulativeCashFlow"].iloc[-1])

    rows: List[dict] = []
    for step in range(1, forecast_periods + 1):
        period = prev_period + pd.DateOffset(months=step)

        revenue = prev_revenue * (1 + rev_growth)
        operating_cost = prev_cost * (1 + cost_growth)

        net_cash_flow = revenue - operating_cost - capex_base - tax_base - wc_base
        cumulative += net_cash_flow

        rows.append(
            {
                "Project": project_name,
                "Period": period,
                "Revenue": revenue,
                "OperatingCost": operating_cost,
                "Capex": capex_base,
                "Tax": tax_base,
                "WorkingCapitalDelta": wc_base,
                "NetCashFlow": net_cash_flow,
                "CumulativeCashFlow": cumulative,
                "Scenario": "Forecast",
            }
        )

        prev_revenue = revenue
        prev_cost = operating_cost

    return pd.DataFrame(rows)


def generate_forecast(actual_df: pd.DataFrame, forecast_periods: int) -> pd.DataFrame:
    parts = [
        forecast_one_project(group, forecast_periods)
        for _, group in actual_df.groupby("Project", sort=True)
    ]
    if not parts:
        return pd.DataFrame(columns=actual_df.columns)
    forecast = pd.concat(parts, ignore_index=True)
    return forecast


def build_powerbi_tables(
    actual_df: pd.DataFrame, forecast_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    fact = pd.concat([actual_df, forecast_df], ignore_index=True)
    fact = fact.sort_values(["Project", "Period", "Scenario"]).reset_index(drop=True)

    dim = (
        fact[["Project"]]
        .drop_duplicates()
        .sort_values("Project")
        .reset_index(drop=True)
    )
    dim["ProjectKey"] = dim.index + 1

    fact = fact.merge(dim, on="Project", how="left")
    fact["IsForecast"] = fact["Scenario"].eq("Forecast")
    fact["Period"] = pd.to_datetime(fact["Period"]).dt.date

    fact = fact[
        [
            "ProjectKey",
            "Project",
            "Period",
            "Scenario",
            "IsForecast",
            "Revenue",
            "OperatingCost",
            "Capex",
            "Tax",
            "WorkingCapitalDelta",
            "NetCashFlow",
            "CumulativeCashFlow",
        ]
    ]

    dim = dim[["ProjectKey", "Project"]]
    return fact, dim


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def create_sample_excel(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    periods = pd.date_range("2025-01-01", periods=12, freq="MS")
    rows: List[dict] = []

    base_data = {
        "Project A": {"rev": 100000, "cost": 55000, "capex": 12000, "tax": 6000, "wc": 2500},
        "Project B": {"rev": 85000, "cost": 50000, "capex": 10000, "tax": 5000, "wc": 1800},
    }

    for project, base in base_data.items():
        for idx, period in enumerate(periods):
            rows.append(
                {
                    "Project": project,
                    "Period": period,
                    "Revenue": base["rev"] * (1 + 0.01 * idx),
                    "OperatingCost": base["cost"] * (1 + 0.008 * idx),
                    "Capex": base["capex"] * (1 + 0.002 * idx),
                    "Tax": base["tax"] * (1 + 0.006 * idx),
                    "WorkingCapitalDelta": base["wc"] * (1 + 0.003 * idx),
                }
            )

    pd.DataFrame(rows).to_excel(path, index=False)


def run_pipeline(input_path: Path, output_dir: Path, forecast_periods: int) -> None:
    source_df = load_input_excel(input_path)
    actual_df = calculate_actual_cashflow(source_df)
    forecast_df = generate_forecast(actual_df, forecast_periods)
    fact_df, dim_df = build_powerbi_tables(actual_df, forecast_df)

    ensure_output_dir(output_dir)

    actual_df.to_csv(output_dir / "cashflow_actual.csv", index=False, encoding="utf-8-sig")
    forecast_df.to_csv(output_dir / "cashflow_forecast.csv", index=False, encoding="utf-8-sig")
    fact_df.to_csv(output_dir / "powerbi_fact_cashflow.csv", index=False, encoding="utf-8-sig")
    dim_df.to_csv(output_dir / "powerbi_dim_project.csv", index=False, encoding="utf-8-sig")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="财务自动化: Excel -> 现金流 -> 预测 -> Power BI")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("input/sample_projects.xlsx"),
        help="输入 Excel 路径",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output"),
        help="输出目录",
    )
    parser.add_argument(
        "--forecast-periods",
        type=int,
        default=12,
        help="预测期数（月）",
    )
    parser.add_argument(
        "--create-sample",
        action="store_true",
        help="先创建示例 Excel 输入文件",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.forecast_periods <= 0:
        raise ValueError("--forecast-periods 必须大于 0")

    if args.create_sample:
        create_sample_excel(args.input)
        print(f"示例文件已创建: {args.input}")

    run_pipeline(args.input, args.output, args.forecast_periods)
    print(f"处理完成。输出目录: {args.output}")


if __name__ == "__main__":
    main()
