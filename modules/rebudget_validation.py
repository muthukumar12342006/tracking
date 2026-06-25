"""Module 4 – Re-Budgeting & Revision Approval Validation."""

import pandas as pd

REQUIRED_COLUMNS = ["Budget Head", "Original Budget", "Revised Budget", "Revision Date", "Approval Status"]


def validate_revisions(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["Original Budget"] = pd.to_numeric(work["Original Budget"], errors="coerce")
    work["Revised Budget"] = pd.to_numeric(work["Revised Budget"], errors="coerce")
    work["Revision Date"] = pd.to_datetime(work["Revision Date"], errors="coerce")
    work["Revision Amount"] = work["Revised Budget"] - work["Original Budget"]
    work["Revision %"] = (
        work["Revision Amount"] / work["Original Budget"].replace(0, pd.NA) * 100
    ).fillna(0).round(2)

    status = work["Approval Status"].astype(str).str.strip().str.lower()

    def classify(s, rev_pct):
        if s in ("approved", "yes", "complete"):
            return "Approved Revision", "Compliant"
        if s in ("pending", "in review", "submitted"):
            return "Pending Approval", "Warning"
        if s in ("", "nan", "none", "missing", "unapproved", "rejected", "no"):
            return "Unapproved Revision", "Critical"
        return "Approval Exception", "Critical"

    results = work.apply(lambda r: classify(str(r["Approval Status"]).lower(), r["Revision %"]), axis=1, result_type="expand")
    work["Revision Category"] = results[0]
    work["Compliance Status"] = results[1]

    work["Critical Breach"] = (
        (work["Compliance Status"] == "Critical")
        & (work["Revision %"].abs() > 5)
    )

    return work


def get_revision_summary(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"approved": 0, "unapproved": 0, "exceptions": 0, "critical": 0}
    return {
        "approved": int((df["Revision Category"] == "Approved Revision").sum()),
        "unapproved": int((df["Revision Category"] == "Unapproved Revision").sum()),
        "exceptions": int((df["Revision Category"] == "Approval Exception").sum()),
        "critical": int(df.get("Critical Breach", pd.Series([False])).sum()),
    }
