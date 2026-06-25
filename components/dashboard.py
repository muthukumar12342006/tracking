"""Main executive dashboard component."""

import numpy as np
import pandas as pd
import streamlit as st

from components.charts import (
    budget_utilization_gauge,
    budget_vs_actual_trend,
    department_spend,
    monthly_variance_trend,
    risk_heatmap,
    variance_waterfall,
)
from components.styles import format_currency, render_header, render_kpi_card


def _compute_kpis(variance_df, approval_df, overspend_df):
    kpis = {
        "total_budget": 0,
        "total_actual": 0,
        "variance": 0,
        "variance_pct": 0,
        "overspent_heads": 0,
        "pending_approvals": 0,
        "high_risk": 0,
    }

    if variance_df is not None and not variance_df.empty:
        kpis["total_budget"] = variance_df["Budget Amount"].sum()
        kpis["total_actual"] = variance_df["Actual Amount"].sum()
        kpis["variance"] = kpis["total_actual"] - kpis["total_budget"]
        if kpis["total_budget"]:
            kpis["variance_pct"] = kpis["variance"] / kpis["total_budget"] * 100
        if "Variance Amount" in variance_df.columns:
            kpis["overspent_heads"] = int((variance_df["Variance Amount"] > 0).sum())
        if "Risk Rating" in variance_df.columns:
            kpis["high_risk"] = int((variance_df["Risk Rating"] == "High").sum())

    if approval_df is not None and not approval_df.empty:
        if "Compliance Status" in approval_df.columns:
            kpis["pending_approvals"] = int((approval_df["Compliance Status"].isin(["Critical", "Warning"])).sum())
        elif "Approval Status" in approval_df.columns:
            kpis["pending_approvals"] = int((approval_df["Approval Status"] == "Missing").sum())

    if overspend_df is not None and not overspend_df.empty and "Risk Level" in overspend_df.columns:
        kpis["high_risk"] += int((overspend_df["Risk Level"].isin(["High", "Critical"])).sum())

    return kpis


def render_dashboard(variance_df, approval_df, overspend_df, theme: str, logo_path: str):
    col_logo, col_title = st.columns([1, 5])
    with col_logo:
        if logo_path:
            st.image(logo_path, width=120)
    with col_title:
        render_header(
            "Executive Dashboard",
            "Real-time budget performance, variance analytics & risk intelligence",
        )

    kpis = _compute_kpis(variance_df, approval_df, overspend_df)

    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)

    with c1:
        render_kpi_card("Total Budget Value", format_currency(kpis["total_budget"]), delay=0)
    with c2:
        render_kpi_card("Total Actual Spend", format_currency(kpis["total_actual"]), delay=1)
    with c3:
        delta_type = "negative" if kpis["variance"] > 0 else "positive"
        render_kpi_card(
            "Overall Variance",
            format_currency(kpis["variance"]),
            f"{kpis['variance_pct']:+.1f}% vs budget",
            delta_type,
            delay=2,
        )
    with c4:
        render_kpi_card("Overspent Budget Heads", str(kpis["overspent_heads"]), delay=3)
    with c5:
        render_kpi_card("Pending Approvals", str(kpis["pending_approvals"]), delta_type="neutral", delay=4)
    with c6:
        render_kpi_card("High-Risk Categories", str(kpis["high_risk"]), delta_type="negative", delay=5)

    st.markdown('<p class="section-title">Performance Analytics</p>', unsafe_allow_html=True)

    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.plotly_chart(budget_vs_actual_trend(variance_df, theme), use_container_width=True)
    with r1c2:
        st.plotly_chart(variance_waterfall(variance_df, theme), use_container_width=True)

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.plotly_chart(department_spend(variance_df, theme), use_container_width=True)
    with r2c2:
        st.plotly_chart(budget_utilization_gauge(variance_df, theme), use_container_width=True)

    r3c1, r3c2 = st.columns(2)
    with r3c1:
        st.plotly_chart(risk_heatmap(variance_df, theme), use_container_width=True)
    with r3c2:
        st.plotly_chart(monthly_variance_trend(variance_df, theme), use_container_width=True)


def render_landing(logo_path: str):
    _, center, _ = st.columns([1, 2, 1])
    with center:
        st.markdown('<div class="landing-hero">', unsafe_allow_html=True)
        if logo_path:
            st.image(logo_path, width=180)
        st.markdown(
            """
            <h1 style="color:#00D4AA;font-size:2.5rem;font-weight:800;margin:0;text-align:center;">Cap AI</h1>
            <p style="color:#94A3B8;font-size:1.2rem;margin-top:0.5rem;text-align:center;">Budgeting & Variance Analytics Platform</p>
            <p style="color:#64748B;font-size:0.95rem;margin-top:1rem;text-align:center;">
                Enterprise-grade financial intelligence for CFOs, Finance Controllers, FP&A teams, and Business Leaders.
            </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="feature-grid">
            <div class="feature-card"><h3>📈 Variance Analysis</h3><p>Identify significant budget vs actual variances with automated risk scoring and executive-ready visualizations.</p></div>
            <div class="feature-card"><h3>✅ Approval Compliance</h3><p>Verify budgets were approved before period start with timeline tracking and compliance dashboards.</p></div>
            <div class="feature-card"><h3>🔴 Overspend Detection</h3><p>Flag chronically overspent budget heads across periods with trend scoring and risk ranking.</p></div>
            <div class="feature-card"><h3>🔄 Re-Budget Validation</h3><p>Audit budget revisions and re-budgeting with full approval trail and exception highlighting.</p></div>
            <div class="feature-card"><h3>🧪 Assumption Testing</h3><p>Test reasonableness of budget assumptions against historical benchmarks with outlier detection.</p></div>
            <div class="feature-card"><h3>📋 Executive Reports</h3><p>Generate PDF, Excel, and PowerPoint-style reports with Cap AI branding and recommendations.</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

