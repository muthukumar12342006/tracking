"""Module 1 – Budget vs Actual Variance Analysis."""

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = ["Budget Head", "Department", "Budget Amount", "Actual Amount", "Period"]


def classify_risk(variance_pct: float) -> str:
    abs_pct = abs(variance_pct)
    if abs_pct < 5:
        return "Low"
    if abs_pct <= 10:
        return "Medium"
    return "High"


def process_variance(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["Budget Amount"] = pd.to_numeric(work["Budget Amount"], errors="coerce")
    work["Actual Amount"] = pd.to_numeric(work["Actual Amount"], errors="coerce")
    work = work.dropna(subset=["Budget Amount", "Actual Amount"])

    work["Variance Amount"] = work["Actual Amount"] - work["Budget Amount"]
    work["Variance %"] = np.where(
        work["Budget Amount"] != 0,
        work["Variance Amount"] / work["Budget Amount"] * 100,
        0,
    )
    work["Variance Type"] = np.where(work["Variance Amount"] <= 0, "Favorable", "Unfavorable")
    work["Favorable Variance"] = np.where(work["Variance Amount"] < 0, abs(work["Variance Amount"]), 0)
    work["Unfavorable Variance"] = np.where(work["Variance Amount"] > 0, work["Variance Amount"], 0)
    work["Risk Rating"] = work["Variance %"].apply(classify_risk)

    return work[
        [
            "Budget Head", "Department", "Budget Amount", "Actual Amount",
            "Period", "Variance Amount", "Variance %", "Variance Type",
            "Favorable Variance", "Unfavorable Variance", "Risk Rating",
        ]
    ]


def get_summary_stats(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}
    return {
        "total_budget": df["Budget Amount"].sum(),
        "total_actual": df["Actual Amount"].sum(),
        "favorable_count": int((df["Variance Type"] == "Favorable").sum()),
        "unfavorable_count": int((df["Variance Type"] == "Unfavorable").sum()),
        "high_risk_count": int((df["Risk Rating"] == "High").sum()),
    }
