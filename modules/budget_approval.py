"""Module 2 – Budget Approval Compliance Validation."""

import pandas as pd

REQUIRED_COLUMNS = ["Budget Head", "Approval Date", "Budget Period Start"]


def validate_approvals(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["Approval Date"] = pd.to_datetime(work["Approval Date"], errors="coerce")
    work["Budget Period Start"] = pd.to_datetime(work["Budget Period Start"], errors="coerce")

    def classify(row):
        if pd.isna(row["Approval Date"]):
            return "Critical", "Missing Approval"
        if pd.isna(row["Budget Period Start"]):
            return "Warning", "Missing Period Start"
        if row["Approval Date"] < row["Budget Period Start"]:
            return "Compliant", "Approved On Time"
        if row["Approval Date"] == row["Budget Period Start"]:
            return "Warning", "Late Approval (Same Day)"
        return "Critical", "Late Approval"

    results = work.apply(classify, axis=1, result_type="expand")
    work["Compliance Status"] = results[0]
    work["Approval Status"] = results[1]

    days_late = (work["Approval Date"] - work["Budget Period Start"]).dt.days
    work["Days From Period Start"] = days_late

    return work


def get_compliance_summary(df: pd.DataFrame) -> dict:
    if df.empty or "Compliance Status" not in df.columns:
        return {"on_time": 0, "late": 0, "missing": 0}
    return {
        "on_time": int((df["Compliance Status"] == "Compliant").sum()),
        "late": int((df["Approval Status"].str.contains("Late", na=False)).sum()),
        "missing": int((df["Approval Status"] == "Missing Approval").sum()),
    }
