"""AG Grid table components with conditional formatting."""

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode

from components.styles import COLORS


def _base_grid_options(df: pd.DataFrame, height: int = 400) -> GridOptionsBuilder:
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(filterable=True, sortable=True, resizable=True, editable=False)
    gb.configure_pagination(enabled=True, paginationPageSize=15)
    gb.configure_selection("single", use_checkbox=False)
    gb.configure_grid_options(domLayout="normal")
    return gb


def render_aggrid(df: pd.DataFrame, key: str, height: int = 400, conditional_cols: dict | None = None):
    if df is None or df.empty:
        st.info("No data to display. Upload a file or load sample data.")
        return None

    gb = _base_grid_options(df, height)

    if conditional_cols:
        for col, rules in conditional_cols.items():
            if col in df.columns:
                js = JsCode(f"""
                function(params) {{
                    if (params.value == null) return {{}};
                    var val = params.value;
                    {rules}
                    return {{}};
                }}
                """)
                gb.configure_column(col, cellStyle=js)

    grid_options = gb.build()
    response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.NO_UPDATE,
        height=height,
        theme="streamlit",
        allow_unsafe_jscode=True,
        key=key,
    )
    return response


def render_variance_table(df: pd.DataFrame, key: str = "variance_grid"):
    if df is None or df.empty:
        st.info("Upload variance data to view the analysis table.")
        return

    display = df.copy()
    for col in ["Budget Amount", "Actual Amount", "Variance Amount"]:
        if col in display.columns:
            display[col] = display[col].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else "")
    if "Variance %" in display.columns:
        display["Variance %"] = display["Variance %"].apply(lambda x: f"{x:+.1f}%" if pd.notna(x) else "")

    gb = GridOptionsBuilder.from_dataframe(display)
    gb.configure_default_column(filterable=True, sortable=True, resizable=True)
    gb.configure_pagination(enabled=True, paginationPageSize=12)

    if "Risk Rating" in display.columns:
        gb.configure_column("Risk Rating", cellStyle=JsCode("""
        function(params) {
            if (params.value === 'Low') return {'backgroundColor': 'rgba(16,185,129,0.25)', 'color': '#10B981', 'fontWeight': '600'};
            if (params.value === 'Medium') return {'backgroundColor': 'rgba(245,158,11,0.25)', 'color': '#F59E0B', 'fontWeight': '600'};
            if (params.value === 'High') return {'backgroundColor': 'rgba(239,68,68,0.25)', 'color': '#EF4444', 'fontWeight': '600'};
            return {};
        }
        """))

    if "Variance Type" in display.columns:
        gb.configure_column("Variance Type", cellStyle=JsCode("""
        function(params) {
            if (params.value === 'Favorable') return {'color': '#10B981', 'fontWeight': '600'};
            if (params.value === 'Unfavorable') return {'color': '#EF4444', 'fontWeight': '600'};
            return {};
        }
        """))

    AgGrid(display, gridOptions=gb.build(), height=420, theme="streamlit", allow_unsafe_jscode=True, key=key)


def render_generic_table(df: pd.DataFrame, key: str, height: int = 400):
    render_aggrid(df, key=key, height=height)


def data_quality_score(df: pd.DataFrame) -> dict:
    if df is None or df.empty:
        return {"score": 0, "missing_cells": 0, "total_cells": 0, "rows": 0, "columns": 0}

    total = df.size
    missing = int(df.isna().sum().sum())
    score = round((1 - missing / total) * 100, 1) if total else 0
    return {
        "score": score,
        "missing_cells": missing,
        "total_cells": total,
        "rows": len(df),
        "columns": len(df.columns),
    }


def validate_columns(df: pd.DataFrame, required: list[str]) -> tuple[bool, list[str]]:
    missing = [c for c in required if c not in df.columns]
    return len(missing) == 0, missing
