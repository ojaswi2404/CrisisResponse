import os
import sys
from datetime import datetime, timedelta

import plotly.express as px
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.auth import login_admin, logout_admin
from utils.state import get_alert_counts, init_session_state
from utils.styles import GLOBAL_CSS, page_header


st.set_page_config(page_title="Admin Dashboard", page_icon="🎛️", layout="wide")


TYPE_CONFIG = {
    "fire": {"label": "Fire", "icon": "🔥", "color": "#ff6b57"},
    "medical": {"label": "Medical", "icon": "🏥", "color": "#37c9ff"},
    "security": {"label": "Security", "icon": "🛡️", "color": "#9b7bff"},
    "other": {"label": "Other", "icon": "⚠️", "color": "#ffb547"},
}


ADMIN_CSS = """
<style>
.admin-shell {
    background: linear-gradient(180deg, rgba(20,24,32,0.96), rgba(15,19,24,0.92));
    border: 1px solid #1e2535;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 16px;
}

.admin-note {
    color: #8a95a8;
    font-size: 0.82rem;
    margin-top: 4px;
}

.group-chip {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    margin-right: 8px;
    border: 1px solid #2a3550;
    background: #141820;
    color: #e8edf5;
}
</style>
"""


def alert_dataframe():
    alerts = st.session_state.get("alerts", [])
    rows = []
    for alert in alerts:
        cfg = TYPE_CONFIG.get(alert["type"], TYPE_CONFIG["other"])
        rows.append(
            {
                "ID": alert["id"],
                "Type": f"{cfg['icon']} {cfg['label']}",
                "Room": alert.get("room") or "Not shared",
                "Location": alert.get("location", "Unknown"),
                "Source": alert.get("source", "SOS Button"),
                "Status": alert["status"].replace("_", " ").title(),
                "Time": alert["timestamp_str"],
                "Description": alert.get("description", ""),
            }
        )
    return rows


def render_sidebar(counts: dict) -> None:
    with st.sidebar:
        st.markdown("## Admin Control")
        st.caption("Live emergency operations")
        st.metric("Total Alerts", counts["total"])
        st.metric("Pending", counts["pending"])
        st.metric("In Progress", counts["in_progress"])
        st.metric("Resolved", counts["resolved"])
        st.info(datetime.now().strftime("%d %b %Y, %I:%M:%S %p"))
        if st.button("Refresh Dashboard", use_container_width=True):
            st.rerun()


def render_overview(counts: dict) -> None:
    cols = st.columns(4)
    cols[0].metric("Fire Alerts", counts["fire"])
    cols[1].metric("Medical Alerts", counts["medical"])
    cols[2].metric("Security Alerts", counts["security"])
    cols[3].metric("Other Alerts", counts["other"])


def render_status_chart(counts: dict) -> None:
    chart_data = {
        "Status": ["Pending", "In Progress", "Resolved"],
        "Count": [counts["pending"], counts["in_progress"], counts["resolved"]],
    }
    fig = px.bar(
        chart_data,
        x="Status",
        y="Count",
        color="Status",
        color_discrete_map={
            "Pending": "#ff6b57",
            "In Progress": "#ffd166",
            "Resolved": "#06d6a0",
        },
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        legend_title_text="",
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_activity_chart(alerts: list[dict]) -> None:
    now = datetime.now()
    labels = [(now - timedelta(hours=i)).strftime("%H:00") for i in range(5, -1, -1)]
    values = []
    for i in range(5, -1, -1):
        start = now - timedelta(hours=i + 1)
        end = now - timedelta(hours=i)
        values.append(sum(1 for alert in alerts if start <= alert["timestamp"] <= end))

    fig = px.line(
        x=labels,
        y=values,
        markers=True,
        labels={"x": "Time", "y": "Alerts"},
    )
    fig.update_traces(line_color="#37c9ff")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_team_panel(group_key: str, title: str) -> None:
    members = st.session_state.get("staff_assignments", {}).get(group_key, [])
    open_alerts = [
        alert for alert in st.session_state.get("alerts", []) if alert["type"] == group_key and alert["status"] != "resolved"
    ]

    with st.container(border=True):
        st.subheader(title)
        if open_alerts:
            st.warning(f"{len(open_alerts)} active alert(s) assigned to this team.")
        else:
            st.success("No active alerts for this team.")

        for member in members:
            st.write(f"- {member}")


def render_contacts() -> None:
    contacts = st.session_state.get("emergency_contacts", [])
    extra_contacts = [
        {"name": "Hotel Security", "number": "Ext. 999", "icon": "🛡️"},
        {"name": "Maintenance", "number": "Ext. 200", "icon": "🔧"},
    ]

    with st.container(border=True):
        st.subheader("Emergency Contacts")
        for contact in contacts + extra_contacts:
            left, right = st.columns([1.4, 1])
            left.write(f"{contact['icon']} {contact['name']}")
            right.write(f"**{contact['number']}**")


def render_recent_alerts() -> None:
    rows = alert_dataframe()
    with st.container(border=True):
        st.subheader("Recent Alert Log")
        if rows:
            st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.info("No alerts yet.")


def app():
    init_session_state()
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown(ADMIN_CSS, unsafe_allow_html=True)

    if not st.session_state.get("admin_logged_in"):
        page_header("ADMIN LOGIN", "Login required for admin dashboard access.", "🔐")
        with st.container(border=True):
            username = st.text_input("Admin Username")
            password = st.text_input("Admin Password", type="password")
            if st.button("Login", use_container_width=True):
                if login_admin(username, password):
                    st.success("Admin login successful.")
                    st.rerun()
                st.error("Invalid admin credentials.")
        return

    alerts = st.session_state.get("alerts", [])
    counts = get_alert_counts()

    render_sidebar(counts)
    page_header("ADMIN CONTROL CENTER", "Clear overview for live emergencies, team routing, and response tracking.", "🎛️")
    top_left, top_right = st.columns([1, 0.2])
    with top_left:
        st.caption("Logged in as `admin`")
    with top_right:
        if st.button("Logout", use_container_width=True):
            logout_admin()
            st.rerun()
    render_overview(counts)

    top_left, top_right = st.columns([1.2, 1], gap="large")
    with top_left:
        with st.container(border=True):
            st.subheader("Alert Status Overview")
            st.caption("Pending, in-progress, and resolved emergency count.")
            render_status_chart(counts)
    with top_right:
        with st.container(border=True):
            st.subheader("Recent Activity")
            st.caption("Alerts received in the last 6 hours.")
            render_activity_chart(alerts)

    st.markdown("### Response Teams")
    team_cols = st.columns(2, gap="large")
    with team_cols[0]:
        render_team_panel("fire", "🔥 Fire Response Team")
        render_team_panel("security", "🛡️ Security Response Team")
    with team_cols[1]:
        render_team_panel("medical", "🏥 Medical Response Team")
        render_team_panel("other", "⚠️ Other Response Team")

    bottom_left, bottom_right = st.columns([1.35, 0.85], gap="large")
    with bottom_left:
        render_recent_alerts()
    with bottom_right:
        render_contacts()


if __name__ == "__main__":
    app()
