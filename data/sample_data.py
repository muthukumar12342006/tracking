"""Generate sample datasets for Cap AI demo mode."""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def get_sample_variance() -> pd.DataFrame:
    return pd.DataFrame({
        "Budget Head": [
            "Personnel Salaries", "Marketing Campaign", "IT Infrastructure", "Office Rent",
            "Travel & Entertainment", "Training Programs", "Software Licenses", "Consulting Fees",
            "Equipment Purchase", "Utilities", "Insurance", "R&D Investment",
        ],
        "Department": [
            "HR", "Marketing", "IT", "Operations", "Sales", "HR", "IT", "Finance",
            "Operations", "Operations", "Finance", "R&D",
        ],
        "Budget Amount": [2500000, 800000, 1200000, 600000, 350000, 200000, 450000, 300000, 500000, 180000, 220000, 900000],
        "Actual Amount": [2450000, 920000, 1350000, 580000, 410000, 195000, 480000, 380000, 620000, 195000, 210000, 1100000],
        "Period": ["Q1-2025"] * 12,
    })


def get_sample_approval() -> pd.DataFrame:
    return pd.DataFrame({
        "Budget Head": [
            "Personnel Salaries", "Marketing Campaign", "IT Infrastructure", "Office Rent",
            "Travel & Entertainment", "Training Programs", "Software Licenses", "Consulting Fees",
        ],
        "Approval Date": [
            "2024-12-15", "2024-12-28", "2025-01-05", "2024-12-20",
            "2025-01-10", "2024-12-18", None, "2024-11-30",
        ],
        "Budget Period Start": [
            "2025-01-01"] * 8,
    })


def get_sample_overspend_history() -> pd.DataFrame:
    rows = []
    heads = ["Marketing Campaign", "IT Infrastructure", "Travel & Entertainment", "Consulting Fees", "R&D Investment"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    budgets = [80000, 120000, 35000, 30000, 90000]
    for head, budget in zip(heads, budgets):
        for i, month in enumerate(months):
            actual = budget * (1.05 + 0.03 * i) if head in ("Marketing Campaign", "IT Infrastructure", "Travel & Entertainment") else budget * (0.95 + 0.01 * i)
            rows.append({"Budget Head": head, "Month": month, "Budget": budget, "Actual": round(actual)})
    return pd.DataFrame(rows)


def get_sample_rebudget() -> pd.DataFrame:
    return pd.DataFrame({
        "Budget Head": [
            "Marketing Campaign", "IT Infrastructure", "Office Rent", "Consulting Fees",
            "Software Licenses", "R&D Investment",
        ],
        "Original Budget": [800000, 1200000, 600000, 300000, 450000, 900000],
        "Revised Budget": [950000, 1200000, 600000, 420000, 450000, 1200000],
        "Revision Date": ["2025-02-15", "2025-01-20", "2025-03-01", "2025-02-28", "2025-01-10", "2025-03-15"],
        "Approval Status": ["Approved", "Approved", "Pending", "Unapproved", "Approved", "Rejected"],
    })


def get_sample_assumptions() -> pd.DataFrame:
    return pd.DataFrame({
        "Budget Head": [
            "Revenue Growth", "Personnel Cost Inflation", "Marketing ROI", "IT CapEx",
            "Office Expansion", "Product Launch", "Supply Chain Costs",
        ],
        "Assumption": [
            "15% YoY revenue growth", "4% annual salary increase", "3:1 marketing ROI",
            "Cloud migration savings 20%", "New office in Q3", "50K new users",
            "5% logistics cost reduction",
        ],
        "Growth Rate": [15.0, 4.0, 25.0, -20.0, 30.0, 45.0, -5.0],
        "Historical Average": [8.5, 3.2, 12.0, -8.0, 10.0, 15.0, -2.0],
    })


def export_sample_files():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    get_sample_variance().to_excel(DATA_DIR / "sample_variance.xlsx", index=False)
    get_sample_approval().to_excel(DATA_DIR / "sample_approval.xlsx", index=False)
    get_sample_overspend_history().to_excel(DATA_DIR / "sample_overspend.xlsx", index=False)
    get_sample_rebudget().to_excel(DATA_DIR / "sample_rebudget.xlsx", index=False)
    get_sample_assumptions().to_excel(DATA_DIR / "sample_assumptions.xlsx", index=False)


if __name__ == "__main__":
    export_sample_files()
    print("Sample files exported to data/")
