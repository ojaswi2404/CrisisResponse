import streamlit as st
from datetime import datetime
import uuid


def init_session_state():
    if "alerts" not in st.session_state:
        st.session_state.alerts = []
    if "staff_assignments" not in st.session_state:
        st.session_state.staff_assignments = {
            "fire": ["Ravi Kumar", "Priya Sharma", "Ankit Singh", "Meera Nair", "Suresh Patel"],
            "medical": ["Dr. Aisha Khan", "Nurse Pooja Iyer", "Amit Desai", "Sunita Rao", "Karan Mehta"],
            "security": ["Vikram Joshi", "Deepak Thakur", "Rohit Verma", "Nalini Das", "Sachin Patil"],
            "other": ["Neha Gupta", "Arjun Pillai", "Rekha Bose", "Manish Tiwari", "Divya Reddy"],
        }
    if "emergency_contacts" not in st.session_state:
        st.session_state.emergency_contacts = [
            {"name": "Police", "number": "100", "icon": "🚔"},
            {"name": "Ambulance", "number": "108", "icon": "🚑"},
            {"name": "Fire Brigade", "number": "101", "icon": "🚒"},
            {"name": "Women Helpline", "number": "1091", "icon": "👩"},
            {"name": "Disaster Mgmt", "number": "1070", "icon": "⚠️"},
        ]
    if "staff_logged_in" not in st.session_state:
        st.session_state.staff_logged_in = False
    if "staff_user" not in st.session_state:
        st.session_state.staff_user = None
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False


def add_alert(alert_type: str, location: str, description: str, source: str = "SOS Button", room: str = ""):
    alert = {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": alert_type,
        "location": location,
        "description": description,
        "source": source,
        "room": room,
        "assigned_group": alert_type,
        "status": "pending",
        "timestamp": datetime.now(),
        "timestamp_str": datetime.now().strftime("%d %b %Y, %I:%M:%S %p"),
        "resolved_at": None,
    }
    if "alerts" not in st.session_state:
        st.session_state.alerts = []
    st.session_state.alerts.insert(0, alert)
    return alert["id"]


def update_alert_status(alert_id: str, new_status: str):
    for alert in st.session_state.alerts:
        if alert["id"] == alert_id:
            alert["status"] = new_status
            if new_status == "resolved":
                alert["resolved_at"] = datetime.now().strftime("%d %b %Y, %I:%M:%S %p")
            break


def get_alert_counts():
    alerts = st.session_state.get("alerts", [])
    counts = {
        "total": len(alerts),
        "pending": sum(1 for a in alerts if a["status"] == "pending"),
        "in_progress": sum(1 for a in alerts if a["status"] == "in_progress"),
        "resolved": sum(1 for a in alerts if a["status"] == "resolved"),
        "fire": sum(1 for a in alerts if a["type"] == "fire"),
        "medical": sum(1 for a in alerts if a["type"] == "medical"),
        "security": sum(1 for a in alerts if a["type"] == "security"),
        "other": sum(1 for a in alerts if a["type"] == "other"),
    }
    return counts
