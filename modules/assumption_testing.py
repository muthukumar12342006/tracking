"""Module 5 – Budget Assumption Reasonableness Testing."""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

REQUIRED_COLUMNS = ["Budget Head", "Assumption", "Growth Rate", "Historical Average"]


def test_assumptions(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["Growth Rate"] = pd.to_numeric(work["Growth Rate"], errors="coerce")
    work["Historical Average"] = pd.to_numeric(work["Historical Average"], errors="coerce")
    work = work.dropna(subset=["Growth Rate", "Historical Average"])

    work["Deviation"] = work["Growth Rate"] - work["Historical Average"]
    work["Deviation %"] = np.where(
        work["Historical Average"] != 0,
        abs(work["Deviation"] / work["Historical Average"] * 100),
        abs(work["Deviation"]),
    )

    # Assumption risk score (0-100)
    work["Assumption Risk Score"] = (
        work["Deviation %"].clip(0, 100) * 0.5
        + (work["Growth Rate"].abs().clip(0, 50)) * 0.3
        + np.where(work["Growth Rate"] > work["Historical Average"] * 2, 20, 0)
    ).clip(0, 100).round(1)

    def reasonableness_rating(score, deviation):
        if score < 25 and abs(deviation) < 5:
            return "Reasonable"
        if score < 50:
            return "Moderate Concern"
        return "High Concern"

    work["Reasonableness Rating"] = work.apply(
        lambda r: reasonableness_rating(r["Assumption Risk Score"], r["Deviation"]), axis=1
    )

    # Outlier detection via Isolation Forest
    if len(work) >= 3:
        features = work[["Growth Rate", "Historical Average", "Deviation %"]].fillna(0)
        iso = IsolationForest(contamination=0.15, random_state=42)
        preds = iso.fit_predict(features)
        work["Outlier Flag"] = np.where(preds == -1, "Outlier", "Normal")
    else:
        work["Outlier Flag"] = "Normal"

    work["Extreme Growth"] = work["Growth Rate"] > work["Historical Average"] * 1.5
    work["Unusual Projection"] = work["Deviation %"] > 30

    return work


def get_assumption_summary(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"reasonable": 0, "moderate": 0, "high_concern": 0, "outliers": 0}
    return {
        "reasonable": int((df["Reasonableness Rating"] == "Reasonable").sum()),
        "moderate": int((df["Reasonableness Rating"] == "Moderate Concern").sum()),
        "high_concern": int((df["Reasonableness Rating"] == "High Concern").sum()),
        "outliers": int((df.get("Outlier Flag", "") == "Outlier").sum()),
    }
