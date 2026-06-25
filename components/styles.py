"""Cap AI – Premium enterprise styling, themes, and UI helpers."""

from pathlib import Path

# Brand palette inspired by Cap AI logo
COLORS = {
    "navy": "#0A1628",
    "navy_light": "#152238",
    "teal": "#00D4AA",
    "teal_dark": "#00A888",
    "gold": "#C9A227",
    "gold_light": "#E8C547",
    "white": "#FFFFFF",
    "gray_100": "#F8FAFC",
    "gray_200": "#E2E8F0",
    "gray_400": "#94A3B8",
    "gray_600": "#475569",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#3B82F6",
}

LOGO_PATH = Path(__file__).resolve().parent.parent / "assets" / "cap_ai_logo.png"

NAV_ITEMS = [
    ("🏠", "Home", "home"),
    ("📊", "Dashboard", "dashboard"),
    ("📈", "Variance Analysis", "variance"),
    ("✅", "Budget Approval", "approval"),
    ("🔴", "Overspend Detection", "overspend"),
    ("🔄", "Re-Budget Validation", "rebudget"),
    ("🧪", "Assumption Testing", "assumptions"),
    ("📁", "Excel Import Center", "import"),
    ("📋", "Executive Reports", "reports"),
]


def init_session_defaults():
    import streamlit as st

    defaults = {
        "theme": "dark",
        "variance_df": None,
        "approval_df": None,
        "overspend_df": None,
        "rebudget_df": None,
        "assumption_df": None,
        "uploaded_datasets": {},
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def get_plotly_template(theme: str) -> str:
    return "plotly_dark" if theme == "dark" else "plotly_white"


def get_css(theme: str) -> str:
    is_dark = theme == "dark"
    bg = COLORS["navy"] if is_dark else COLORS["gray_100"]
    card_bg = "rgba(21, 34, 56, 0.65)" if is_dark else "rgba(255, 255, 255, 0.75)"
    card_border = "rgba(0, 212, 170, 0.25)" if is_dark else "rgba(10, 22, 40, 0.12)"
    text = COLORS["white"] if is_dark else COLORS["navy"]
    text_muted = COLORS["gray_400"] if is_dark else COLORS["gray_600"]
    sidebar_bg = COLORS["navy_light"] if is_dark else COLORS["white"]

    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background: {bg};
        background-image: {'radial-gradient(ellipse at 20% 0%, rgba(0,212,170,0.08) 0%, transparent 50%), radial-gradient(ellipse at 80% 100%, rgba(201,162,39,0.06) 0%, transparent 50%)' if is_dark else 'radial-gradient(ellipse at 20% 0%, rgba(0,212,170,0.06) 0%, transparent 50%)'};
    }}

    [data-testid="stSidebar"] {{
        background: {sidebar_bg};
        border-right: 1px solid {card_border};
    }}

    [data-testid="stSidebar"] .stMarkdown h1, [data-testid="stSidebar"] .stMarkdown h2 {{
        color: {COLORS['teal']};
    }}

    .cap-header {{
        background: linear-gradient(135deg, {COLORS['navy']} 0%, {COLORS['navy_light']} 50%, rgba(0,212,170,0.15) 100%);
        border: 1px solid {card_border};
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }}

    .cap-header h1 {{
        color: {text};
        font-weight: 800;
        font-size: 2rem;
        margin: 0;
        letter-spacing: -0.02em;
    }}

    .cap-header p {{
        color: {text_muted};
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
    }}

    .glass-card {{
        background: {card_bg};
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid {card_border};
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        box-shadow: 0 4px 24px rgba(0,0,0,0.12);
    }}

    .glass-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0,212,170,0.15);
        border-color: rgba(0,212,170,0.4);
    }}

    .kpi-card {{
        background: {card_bg};
        backdrop-filter: blur(16px);
        border: 1px solid {card_border};
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.6s ease forwards;
        opacity: 0;
    }}

    .kpi-card:hover {{
        transform: scale(1.03);
        border-color: {COLORS['teal']};
        box-shadow: 0 8px 30px rgba(0,212,170,0.2);
    }}

    .kpi-value {{
        font-size: 1.75rem;
        font-weight: 700;
        color: {COLORS['teal']};
        line-height: 1.2;
    }}

    .kpi-label {{
        font-size: 0.8rem;
        color: {text_muted};
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 0.35rem;
        font-weight: 500;
    }}

    .kpi-delta {{
        font-size: 0.85rem;
        margin-top: 0.5rem;
        font-weight: 600;
    }}

    .kpi-delta.positive {{ color: {COLORS['success']}; }}
    .kpi-delta.negative {{ color: {COLORS['danger']}; }}
    .kpi-delta.neutral {{ color: {COLORS['warning']}; }}

    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .kpi-card:nth-child(1) {{ animation-delay: 0.05s; }}
    .kpi-card:nth-child(2) {{ animation-delay: 0.1s; }}
    .kpi-card:nth-child(3) {{ animation-delay: 0.15s; }}
    .kpi-card:nth-child(4) {{ animation-delay: 0.2s; }}
    .kpi-card:nth-child(5) {{ animation-delay: 0.25s; }}
    .kpi-card:nth-child(6) {{ animation-delay: 0.3s; }}

    .section-title {{
        color: {text};
        font-weight: 700;
        font-size: 1.35rem;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid {COLORS['teal']};
        display: inline-block;
    }}

    .badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}

    .badge-low {{ background: rgba(16,185,129,0.2); color: {COLORS['success']}; }}
    .badge-medium {{ background: rgba(245,158,11,0.2); color: {COLORS['warning']}; }}
    .badge-high {{ background: rgba(239,68,68,0.2); color: {COLORS['danger']}; }}
    .badge-critical {{ background: rgba(239,68,68,0.35); color: #FCA5A5; }}

    .landing-hero {{
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, rgba(10,22,40,0.9) 0%, rgba(21,34,56,0.85) 100%);
        border-radius: 20px;
        border: 1px solid {card_border};
        margin-bottom: 2rem;
    }}

    .feature-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.25rem;
    }}

    .feature-card {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 14px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }}

    .feature-card:hover {{
        border-color: {COLORS['gold']};
        transform: translateY(-3px);
    }}

    .feature-card h3 {{
        color: {COLORS['teal']};
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }}

    .feature-card p {{
        color: {text_muted};
        font-size: 0.9rem;
        line-height: 1.5;
    }}

    div[data-testid="stMetric"] {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 12px;
        padding: 1rem;
    }}

    .stDownloadButton button {{
        background: linear-gradient(135deg, {COLORS['teal']} 0%, {COLORS['teal_dark']} 100%) !important;
        color: {COLORS['navy']} !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
    }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
    """


def render_kpi_card(label: str, value: str, delta: str = "", delta_type: str = "neutral", delay: int = 0):
    import streamlit as st

    delta_class = delta_type if delta_type in ("positive", "negative", "neutral") else "neutral"
    st.markdown(
        f"""
        <div class="kpi-card" style="animation-delay: {delay * 0.05}s;">
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
            {f'<div class="kpi-delta {delta_class}">{delta}</div>' if delta else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_header(title: str, subtitle: str = ""):
    import streamlit as st

    st.markdown(
        f"""
        <div class="cap-header">
            <h1>{title}</h1>
            {f'<p>{subtitle}</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def format_currency(value: float) -> str:
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:,.2f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:,.1f}K"
    return f"${value:,.0f}"


def format_pct(value: float) -> str:
    return f"{value:+.1f}%"


def risk_badge(risk: str) -> str:
    mapping = {
        "low": "badge-low",
        "medium": "badge-medium",
        "high": "badge-high",
        "critical": "badge-critical",
        "compliant": "badge-low",
        "warning": "badge-medium",
        "reasonable": "badge-low",
        "moderate concern": "badge-medium",
        "high concern": "badge-high",
    }
    css = mapping.get(risk.lower(), "badge-medium")
    return f'<span class="badge {css}">{risk}</span>'
