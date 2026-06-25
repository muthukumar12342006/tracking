"""Plotly chart components for Cap AI platform."""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from components.styles import COLORS, get_plotly_template


def _layout(fig, theme: str, title: str = "", height: int = 420):
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=COLORS["teal"])),
        template=get_plotly_template(theme),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(family="Inter, sans-serif"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def budget_vs_actual_trend(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    if df is None or df.empty:
        return _empty_chart("Upload variance data to view trend", theme)

    work = df.copy()
    if "Period" in work.columns:
        grouped = work.groupby("Period", as_index=False).agg({"Budget Amount": "sum", "Actual Amount": "sum"})
        x_col = "Period"
    else:
        grouped = pd.DataFrame({"Month": ["Total"], "Budget Amount": [work["Budget Amount"].sum()], "Actual Amount": [work["Actual Amount"].sum()]})
        x_col = "Month"

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=grouped[x_col], y=grouped["Budget Amount"], name="Budget", mode="lines+markers", line=dict(color=COLORS["teal"], width=3)))
    fig.add_trace(go.Scatter(x=grouped[x_col], y=grouped["Actual Amount"], name="Actual", mode="lines+markers", line=dict(color=COLORS["gold"], width=3)))
    return _layout(fig, theme, "Budget vs Actual Trend")


def variance_waterfall(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    if df is None or df.empty or "Department" not in df.columns:
        return _empty_chart("Upload variance data for waterfall", theme)

    dept = df.groupby("Department").agg({"Budget Amount": "sum", "Actual Amount": "sum"}).reset_index()
    dept["Variance"] = dept["Actual Amount"] - dept["Budget Amount"]
    dept = dept.sort_values("Variance")

    fig = go.Figure(go.Waterfall(
        x=dept["Department"],
        y=dept["Variance"],
        measure=["relative"] * len(dept),
        increasing=dict(marker=dict(color=COLORS["danger"])),
        decreasing=dict(marker=dict(color=COLORS["success"])),
        connector=dict(line=dict(color=COLORS["gray_400"])),
    ))
    return _layout(fig, theme, "Variance Waterfall by Department")


def department_spend(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    if df is None or df.empty or "Department" not in df.columns:
        return _empty_chart("Upload variance data for department analysis", theme)

    dept = df.groupby("Department").agg({"Budget Amount": "sum", "Actual Amount": "sum"}).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Budget", x=dept["Department"], y=dept["Budget Amount"], marker_color=COLORS["teal"]))
    fig.add_trace(go.Bar(name="Actual", x=dept["Department"], y=dept["Actual Amount"], marker_color=COLORS["gold"]))
    fig.update_layout(barmode="group")
    return _layout(fig, theme, "Department-wise Spend Analysis")


def budget_utilization_gauge(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    if df is None or df.empty:
        return _empty_chart("Upload data for utilization gauge", theme)

    total_budget = df["Budget Amount"].sum()
    total_actual = df["Actual Amount"].sum()
    utilization = min((total_actual / total_budget * 100) if total_budget else 0, 150)

    color = COLORS["success"] if utilization <= 100 else COLORS["danger"]
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=utilization,
        number=dict(suffix="%", font=dict(size=28)),
        delta=dict(reference=100, increasing=dict(color=COLORS["danger"]), decreasing=dict(color=COLORS["success"])),
        gauge=dict(
            axis=dict(range=[0, 150], tickwidth=1),
            bar=dict(color=color),
            steps=[
                dict(range=[0, 80], color="rgba(16,185,129,0.3)"),
                dict(range=[80, 100], color="rgba(245,158,11,0.3)"),
                dict(range=[100, 150], color="rgba(239,68,68,0.3)"),
            ],
            threshold=dict(line=dict(color=COLORS["danger"], width=4), value=100),
        ),
        title=dict(text="Budget Utilization"),
    ))
    return _layout(fig, theme, "", height=350)


def risk_heatmap(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    if df is None or df.empty:
        return _empty_chart("Upload variance data for risk heatmap", theme)

    work = df.copy()
    if "Variance %" not in work.columns and "Budget Amount" in work.columns:
        work["Variance %"] = np.where(
            work["Budget Amount"] != 0,
            abs((work["Actual Amount"] - work["Budget Amount"]) / work["Budget Amount"] * 100),
            0,
        )

    if "Department" not in work.columns:
        return _empty_chart("Department column required for heatmap", theme)

    pivot = work.pivot_table(index="Budget Head", columns="Department", values="Variance %", aggfunc="mean", fill_value=0)
    fig = px.imshow(pivot.values, x=pivot.columns, y=pivot.index, color_continuous_scale=["#10B981", "#F59E0B", "#EF4444"], aspect="auto")
    fig.update_layout(xaxis_title="Department", yaxis_title="Budget Head")
    return _layout(fig, theme, "Risk Heatmap (Variance %)")


def monthly_variance_trend(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    if df is None or df.empty:
        return _empty_chart("Upload data for monthly variance trend", theme)

    work = df.copy()
    period_col = "Period" if "Period" in work.columns else ("Month" if "Month" in work.columns else None)
    if not period_col:
        return _empty_chart("Period/Month column required", theme)

    work["Variance"] = work["Actual Amount"] - work["Budget Amount"] if "Actual Amount" in work.columns else work.get("Variance", 0)
    grouped = work.groupby(period_col)["Variance"].sum().reset_index()

    colors = [COLORS["success"] if v <= 0 else COLORS["danger"] for v in grouped["Variance"]]
    fig = go.Figure(go.Bar(x=grouped[period_col], y=grouped["Variance"], marker_color=colors))
    return _layout(fig, theme, "Monthly Variance Trend")


def variance_bar_chart(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    if df is None or df.empty:
        return _empty_chart("No variance data", theme)

    work = df.nlargest(15, "Variance Amount", keep="all") if "Variance Amount" in df.columns else df.head(15)
    colors = [COLORS["success"] if v <= 0 else COLORS["danger"] for v in work.get("Variance Amount", [0])]
    fig = go.Figure(go.Bar(
        x=work.get("Variance Amount", work.iloc[:, 0]),
        y=work.get("Budget Head", work.index),
        orientation="h",
        marker_color=colors,
    ))
    fig.update_layout(yaxis=dict(autorange="reversed"))
    return _layout(fig, theme, "Variance by Budget Head")


def variance_heatmap_module(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    return risk_heatmap(df, theme)


def approval_timeline(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    if df is None or df.empty:
        return _empty_chart("Upload approval data", theme)

    work = df.copy()
    work["Approval Date"] = pd.to_datetime(work["Approval Date"], errors="coerce")
    work["Budget Period Start"] = pd.to_datetime(work["Budget Period Start"], errors="coerce")
    work = work.dropna(subset=["Budget Period Start"])
    work = work.sort_values("Approval Date")

    fig = go.Figure()
    for status, color in [("Compliant", COLORS["success"]), ("Warning", COLORS["warning"]), ("Critical", COLORS["danger"])]:
        subset = work[work.get("Compliance Status", "") == status]
        if not subset.empty:
            fig.add_trace(go.Scatter(
                x=subset["Approval Date"],
                y=subset["Budget Head"],
                mode="markers",
                name=status,
                marker=dict(size=12, color=color),
            ))
    fig.add_trace(go.Scatter(
        x=work["Budget Period Start"],
        y=work["Budget Head"],
        mode="markers",
        name="Period Start",
        marker=dict(symbol="diamond", size=10, color=COLORS["info"]),
    ))
    return _layout(fig, theme, "Approval Timeline")


def approval_compliance_dashboard(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    if df is None or df.empty or "Compliance Status" not in df.columns:
        return _empty_chart("Run approval validation first", theme)

    counts = df["Compliance Status"].value_counts()
    colors_map = {"Compliant": COLORS["success"], "Warning": COLORS["warning"], "Critical": COLORS["danger"]}
    fig = go.Figure(go.Pie(
        labels=counts.index,
        values=counts.values,
        hole=0.45,
        marker=dict(colors=[colors_map.get(c, COLORS["gray_400"]) for c in counts.index]),
    ))
    return _layout(fig, theme, "Approval Compliance", height=380)


def overspend_trend(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    if df is None or df.empty:
        return _empty_chart("Upload historical budget data", theme)

    work = df.copy()
    work["Overspend"] = (work["Actual"] > work["Budget"]).astype(int)
    trend = work.groupby("Month")["Overspend"].sum().reset_index()
    fig = go.Figure(go.Scatter(x=trend["Month"], y=trend["Overspend"], mode="lines+markers+area", fill="tozeroy", line=dict(color=COLORS["danger"], width=2)))
    return _layout(fig, theme, "Overspending Trend")


def department_risk_ranking(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    if df is None or df.empty or "Risk Score" not in df.columns:
        return _empty_chart("Run overspend analysis first", theme)

    ranked = df.nlargest(10, "Risk Score")
    fig = go.Figure(go.Bar(x=ranked["Risk Score"], y=ranked["Budget Head"], orientation="h", marker_color=COLORS["danger"]))
    fig.update_layout(yaxis=dict(autorange="reversed"))
    return _layout(fig, theme, "Top Risk Budget Heads")


def monthly_breach_chart(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    if df is None or df.empty:
        return _empty_chart("Upload historical data", theme)

    work = df.copy()
    work["Breach"] = np.where(work["Actual"] > work["Budget"], 1, 0)
    monthly = work.groupby("Month")["Breach"].sum().reset_index()
    fig = go.Figure(go.Bar(x=monthly["Month"], y=monthly["Breach"], marker_color=COLORS["warning"]))
    return _layout(fig, theme, "Monthly Budget Breaches")


def revision_audit_trail(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    if df is None or df.empty:
        return _empty_chart("Upload revision register", theme)

    work = df.copy()
    work["Revision Date"] = pd.to_datetime(work["Revision Date"], errors="coerce")
    work = work.sort_values("Revision Date")
    work["Change"] = work["Revised Budget"] - work["Original Budget"]
    colors = [COLORS["success"] if s == "Approved" else COLORS["danger"] for s in work.get("Approval Status", ["Pending"] * len(work))]

    fig = go.Figure(go.Bar(x=work["Budget Head"], y=work["Change"], marker_color=colors))
    return _layout(fig, theme, "Revision Audit Trail")


def revision_trend(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    if df is None or df.empty:
        return _empty_chart("Upload revision data", theme)

    work = df.copy()
    work["Revision Date"] = pd.to_datetime(work["Revision Date"], errors="coerce")
    monthly = work.groupby(work["Revision Date"].dt.to_period("M").astype(str)).size().reset_index(name="Count")
    fig = go.Figure(go.Scatter(x=monthly["Revision Date"], y=monthly["Count"], mode="lines+markers", line=dict(color=COLORS["gold"], width=3)))
    return _layout(fig, theme, "Revision Trend Analysis")


def assumption_comparison(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    if df is None or df.empty:
        return _empty_chart("Upload assumption data", theme)

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Growth Rate", x=df["Budget Head"], y=df["Growth Rate"], marker_color=COLORS["teal"]))
    fig.add_trace(go.Bar(name="Historical Avg", x=df["Budget Head"], y=df["Historical Average"], marker_color=COLORS["gold"]))
    fig.update_layout(barmode="group")
    return _layout(fig, theme, "Assumption vs Historical Benchmark")


def forecast_reliability(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    if df is None or df.empty or "Assumption Risk Score" not in df.columns:
        return _empty_chart("Run assumption testing first", theme)

    fig = go.Figure(go.Scatter(
        x=df["Historical Average"],
        y=df["Growth Rate"],
        mode="markers+text",
        text=df["Budget Head"],
        textposition="top center",
        marker=dict(size=df["Assumption Risk Score"] * 3 + 8, color=df["Assumption Risk Score"], colorscale="RdYlGn_r", showscale=True),
    ))
    fig.update_layout(xaxis_title="Historical Average (%)", yaxis_title="Growth Rate (%)")
    return _layout(fig, theme, "Forecast Reliability Dashboard")


def _empty_chart(message: str, theme: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=message, xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(size=14, color=COLORS["gray_400"]))
    return _layout(fig, theme, "", height=300)
