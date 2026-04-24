import streamlit as st

from utils.auth import ADMIN_CREDENTIALS, STAFF_CREDENTIALS
from utils.state import init_session_state
from utils.styles import GLOBAL_CSS


st.set_page_config(
    page_title="CrisisResponse",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .home-wrap {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 10px 20px;
    }

    .home-shell {
        width: min(760px, 100%);
        text-align: center;
    }

    .logo-badge {
        width: 98px;
        height: 98px;
        margin: 0 auto 18px;
        border-radius: 30px;
        background: radial-gradient(circle at 30% 30%, #5cc8ff 0%, #00a8ff 42%, #0f6ea8 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 0 10px rgba(0,168,255,0.08), 0 18px 40px rgba(0,168,255,0.18);
        position: relative;
    }

    .logo-badge::before {
        content: '';
        width: 56px;
        height: 64px;
        background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(220,242,255,0.95));
        clip-path: polygon(50% 0%, 92% 16%, 92% 56%, 50% 100%, 8% 56%, 8% 16%);
        display: block;
    }

    .home-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 4.2rem;
        font-weight: 700;
        color: #e8edf5;
        letter-spacing: 1px;
        line-height: 1;
        margin-bottom: 12px;
    }

    .home-title span {
        color: #00a8ff;
    }

    .home-tagline {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.95rem;
        color: #c0cad8;
        margin-bottom: 14px;
    }

    .section-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: #e8edf5;
        margin-bottom: 8px;
        letter-spacing: 1px;
    }

    .credentials-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-top: 10px;
        text-align: left;
    }

    .credential-card {
        background: #141820;
        border: 1px solid #1e2535;
        border-radius: 18px;
        padding: 16px;
    }

    .credential-card-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #e8edf5;
        margin-bottom: 10px;
        text-align: center;
    }

    .credential-line {
        padding: 8px 10px;
        border-radius: 10px;
        background: #11161d;
        border: 1px solid #1e2535;
        margin-bottom: 8px;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.84rem;
        color: #c0cad8;
    }

    .credential-line strong {
        color: #e8edf5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

staff_rows = "".join(
    f"<div class='credential-line'><strong>{item['label']}</strong><br>{username} / {item['password']}</div>"
    for username, item in STAFF_CREDENTIALS.items()
)

st.markdown(
    f"""
    <div class="home-wrap">
        <div class="home-shell">
            <div class="logo-badge"></div>
            <div class="home-title">Crisis<span>Response</span></div>
            <div class="home-tagline">One alert. The right team. Immediate action.</div>
            <div class="section-title">Demo Login Credentials</div>
            <div class="credentials-grid">
                <div class="credential-card">
                    <div class="credential-card-title">Admin</div>
                    <div class="credential-line"><strong>Username</strong><br>{ADMIN_CREDENTIALS['username']}</div>
                    <div class="credential-line"><strong>Password</strong><br>{ADMIN_CREDENTIALS['password']}</div>
                </div>
                <div class="credential-card">
                    <div class="credential-card-title">Staff</div>
                    {staff_rows}
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
