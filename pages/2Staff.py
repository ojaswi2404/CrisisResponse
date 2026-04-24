import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.auth import login_staff, logout_staff
from utils.state import get_alert_counts, init_session_state, update_alert_status
from utils.styles import GLOBAL_CSS, page_header


st.set_page_config(page_title="Staff Dashboard", page_icon="👷", layout="wide")


TYPE_LABELS = {
    "fire": "Fire Staff",
    "medical": "Medical Staff",
    "security": "Security Staff",
    "other": "Other Staff",
}


def login_screen():
    page_header("STAFF LOGIN", "Login required for staff dashboard access.", "🔐")
    with st.container(border=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            user = login_staff(username, password)
            if user:
                st.success(f"Logged in as {user['label']}.")
                st.rerun()
            st.error("Invalid staff credentials.")


def dashboard():
    user = st.session_state.staff_user
    group = user["group"]
    alerts = [
        alert for alert in st.session_state.get("alerts", [])
        if alert.get("assigned_group", alert.get("type")) == group
    ]
    counts = get_alert_counts()

    page_header("STAFF DASHBOARD", f"Showing only alerts assigned to {TYPE_LABELS[group]}.", "🚨")

    top_left, top_right = st.columns([1, 0.25])
    with top_left:
        st.caption(f"Logged in as `{user['username']}`")
    with top_right:
        if st.button("Logout", use_container_width=True):
            logout_staff()
            st.rerun()

    metric_cols = st.columns(4)
    metric_cols[0].metric("All Alerts", counts["total"])
    metric_cols[1].metric("My Group Alerts", len(alerts))
    metric_cols[2].metric("Pending", sum(1 for a in alerts if a["status"] == "pending"))
    metric_cols[3].metric("Resolved", sum(1 for a in alerts if a["status"] == "resolved"))

    if not alerts:
        st.info("No alerts assigned to your staff group.")
        return

    for alert in alerts:
        with st.container(border=True):
            st.subheader(f"{alert['id']} • {TYPE_LABELS[group]}")
            st.write(f"Room: **{alert.get('room') or alert.get('location', 'Unknown')}**")
            st.write(f"Message: {alert['description']}")
            st.caption(f"Source: {alert.get('source', 'Voice Report')} | Time: {alert['timestamp_str']}")
            st.caption(f"Status: {alert['status'].replace('_', ' ').title()}")

            col1, col2 = st.columns(2)
            with col1:
                if alert["status"] != "in_progress":
                    if st.button("Mark In Progress", key=f"prog_{alert['id']}", use_container_width=True):
                        update_alert_status(alert["id"], "in_progress")
                        st.rerun()
            with col2:
                if alert["status"] != "resolved":
                    if st.button("Mark Resolved", key=f"res_{alert['id']}", use_container_width=True):
                        update_alert_status(alert["id"], "resolved")
                        st.rerun()


def app():
    init_session_state()
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    if st.session_state.get("staff_logged_in") and st.session_state.get("staff_user"):
        dashboard()
    else:
        login_screen()


if __name__ == "__main__":
    app()
