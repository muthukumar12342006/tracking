"""Module 3 – Chronic Overspend Detection."""

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = ["Budget Head", "Month", "Budget", "Actual"]


def process_overspend(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["Budget"] = pd.to_numeric(work["Budget"], errors="coerce")
    work["Actual"] = pd.to_numeric(work["Actual"], errors="coerce")
    work = work.dropna(subset=["Budget", "Actual"])
    work["Overspent"] = work["Actual"] > work["Budget"]
    work["Overspend %"] = np.where(
        work["Budget"] != 0,
        (work["Actual"] - work["Budget"]) / work["Budget"] * 100,
        0,
    )

    agg = work.groupby("Budget Head").agg(
        Overspend_Frequency=("Overspent", "sum"),
        Total_Periods=("Overspent", "count"),
        Avg_Overspend_Pct=("Overspend %", lambda x: x[x > 0].mean() if (x > 0).any() else 0),
        Max_Overspend_Pct=("Overspend %", "max"),
    ).reset_index()

    agg.rename(columns={
        "Overspend_Frequency": "Overspend Frequency",
        "Avg_Overspend_Pct": "Average Overspend %",
        "Max_Overspend_Pct": "Max Overspend %",
        "Total_Periods": "Total Periods",
    }, inplace=True)

    agg["Overspend Rate"] = agg["Overspend Frequency"] / agg["Total Periods"] * 100

    # Trend score: increasing overspend over time
    trend_scores = []
    for head in agg["Budget Head"]:
        subset = work[work["Budget Head"] == head].sort_values("Month")
        if len(subset) >= 2:
            overspend_series = subset["Overspend"].astype(int).values
            trend = np.polyfit(range(len(overspend_series)), overspend_series, 1)[0]
            trend_scores.append(round(trend * 100, 2))
        else:
            trend_scores.append(0)
    agg["Trend Score"] = trend_scores

    agg["Risk Score"] = (
        agg["Overspend Rate"] * 0.4
        + agg["Average Overspend %"].clip(0, 50) * 0.3
        + agg["Trend Score"].clip(0, 100) * 0.3
    ).round(1)

    def risk_level(score, freq_rate):
        if freq_rate >= 75 or score >= 60:
            return "Critical"
        if freq_rate >= 50 or score >= 40:
            return "High"
        if freq_rate >= 25 or score >= 20:
            return "Medium"
        return "Low"

    agg["Risk Level"] = agg.apply(lambda r: risk_level(r["Risk Score"], r["Overspend Rate"]), axis=1)
    agg = agg[agg["Overspend Frequency"] > 0].sort_values("Risk Score", ascending=False)

    return agg


def get_chronic_overspenders(df: pd.DataFrame, min_frequency: int = 2) -> pd.DataFrame:
    if "Overspend Frequency" not in df.columns:
        return df
    return df[df["Overspend Frequency"] >= min_frequency]
