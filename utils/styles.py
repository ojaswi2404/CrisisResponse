GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #0a0c10;
    --bg-secondary: #0f1318;
    --bg-card: #141820;
    --bg-card-hover: #1a2030;
    --border: #1e2535;
    --border-bright: #2a3550;
    --text-primary: #e8edf5;
    --text-secondary: #8a95a8;
    --text-muted: #4a5568;
    --accent-red: #ff3b3b;
    --accent-orange: #ff8c00;
    --accent-blue: #00a8ff;
    --accent-green: #00e676;
    --accent-purple: #7c4dff;
    --accent-yellow: #ffd600;
    --fire: #ff4500;
    --medical: #00bcd4;
    --security: #7c4dff;
    --other: #ff9800;
    --glow-red: 0 0 20px rgba(255,59,59,0.4);
    --glow-blue: 0 0 20px rgba(0,168,255,0.3);
    --glow-green: 0 0 20px rgba(0,230,118,0.3);
}

html, body, .stApp {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stApp { background-color: var(--bg-primary) !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* Remove streamlit default padding */
.main .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 1400px !important; }

/* Headers */
h1, h2, h3, h4, h5, h6 { font-family: 'Rajdhani', sans-serif !important; color: var(--text-primary) !important; }

/* Input fields */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > select {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-bright) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Buttons */
.stButton > button {
    border-radius: 8px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s ease !important;
    border: 1px solid var(--border-bright) !important;
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
}
.stButton > button:hover {
    border-color: var(--accent-blue) !important;
    box-shadow: var(--glow-blue) !important;
    transform: translateY(-1px) !important;
}

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }

/* Metric cards */
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
[data-testid="metric-container"] label { color: var(--text-secondary) !important; font-family: 'DM Sans', sans-serif !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: var(--text-primary) !important; font-family: 'Rajdhani', sans-serif !important; font-size: 2rem !important; }

/* Selectbox */
.stSelectbox label, .stTextInput label, .stTextArea label { color: var(--text-secondary) !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.85rem !important; }

/* Plotly chart background */
.js-plotly-plot { background: transparent !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-blue); }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border-radius: 8px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
}
.stTabs [aria-selected="true"] {
    background: var(--bg-card-hover) !important;
    color: var(--text-primary) !important;
}

/* Alerts/Info boxes */
.stSuccess, .stInfo, .stWarning, .stError { border-radius: 10px !important; font-family: 'DM Sans', sans-serif !important; }

/* Divider */
hr { border-color: var(--border) !important; }
</style>
"""


def page_header(title: str, subtitle: str, icon: str):
    import streamlit as st
    st.markdown(f"""
    <div style="
        display: flex; align-items: center; gap: 16px;
        padding: 20px 24px; margin-bottom: 24px;
        background: linear-gradient(135deg, #141820 0%, #0f1318 100%);
        border: 1px solid #1e2535; border-radius: 16px;
        border-left: 4px solid #00a8ff;
    ">
        <div style="font-size: 2.5rem;">{icon}</div>
        <div>
            <div style="font-family: 'Rajdhani', sans-serif; font-size: 1.8rem; font-weight: 700; color: #e8edf5; line-height: 1;">{title}</div>
            <div style="font-family: 'DM Sans', sans-serif; font-size: 0.85rem; color: #8a95a8; margin-top: 4px;">{subtitle}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def card(content_html: str, border_color: str = "#1e2535", glow: str = "none", padding: str = "20px"):
    import streamlit as st
    st.markdown(f"""
    <div style="
        background: #141820;
        border: 1px solid {border_color};
        border-radius: 14px;
        padding: {padding};
        box-shadow: {glow};
        margin-bottom: 12px;
    ">{content_html}</div>
    """, unsafe_allow_html=True)
