import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.speech import transcribe_audio
from utils.state import add_alert, init_session_state
from utils.styles import GLOBAL_CSS, page_header


st.set_page_config(page_title="Guest SOS", page_icon="🎙️", layout="wide")


VOICE_CSS = """
<style>
.guest-section-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 2px;
    color: #8a95a8;
    text-transform: uppercase;
    margin: 4px 0 14px;
}

.panic-card {
    min-height: 150px;
    border-radius: 20px;
    padding: 22px 16px;
    position: relative;
    overflow: hidden;
    text-align: center;
    border: 1px solid #2a3550;
    margin-bottom: 6px;
}

.panic-icon {
    font-size: 3.1rem;
    line-height: 1;
    position: relative;
    z-index: 2;
}

.panic-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    letter-spacing: 3px;
    margin-top: 8px;
    position: relative;
    z-index: 2;
}

.panic-desc {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.8rem;
    opacity: 0.8;
    margin-top: 4px;
    position: relative;
    z-index: 2;
}

.panic-ring {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 2px solid currentColor;
    opacity: 0.16;
}

.panic-ring-2 {
    width: 160px;
    height: 160px;
    opacity: 0.08;
}

.panic-button button {
    min-height: 48px !important;
    border-radius: 8px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
}

.voice-box {
    background: #141820;
    border: 1px solid #1e2535;
    border-radius: 16px;
    padding: 22px;
    margin-top: 12px;
}

.voice-note {
    color: #8a95a8;
    font-size: 0.82rem;
    margin-bottom: 14px;
}
</style>
"""


ROOM_OPTIONS = [
    "Room 101",
    "Room 102",
    "Room 201",
    "Room 204",
    "Room 305",
    "Reception",
    "Lobby",
    "Parking",
]


PANIC_BUTTONS = [
    {
        "type": "fire",
        "card_title": "FIRE",
        "button_title": "🔥 FIRE EMERGENCY",
        "icon": "🔥",
        "desc": "Report fire or smoke",
        "color": "#ff6b35",
        "bg": "radial-gradient(ellipse at 50% 35%, rgba(255,107,53,0.18) 0%, #141820 72%)",
    },
    {
        "type": "medical",
        "card_title": "MEDICAL",
        "button_title": "🏥 MEDICAL EMERGENCY",
        "icon": "🏥",
        "desc": "Request medical aid",
        "color": "#25d0ff",
        "bg": "radial-gradient(ellipse at 50% 35%, rgba(37,208,255,0.18) 0%, #141820 72%)",
    },
    {
        "type": "security",
        "card_title": "SECURITY",
        "button_title": "🔒 SECURITY THREAT",
        "icon": "🔒",
        "desc": "Security threat alert",
        "color": "#7b4dff",
        "bg": "radial-gradient(ellipse at 50% 35%, rgba(123,77,255,0.18) 0%, #141820 72%)",
    },
    {
        "type": "other",
        "card_title": "OTHER",
        "button_title": "⚠️ OTHER EMERGENCY",
        "icon": "⚠️",
        "desc": "General emergency",
        "color": "#f5a623",
        "bg": "radial-gradient(ellipse at 50% 35%, rgba(245,166,35,0.18) 0%, #141820 72%)",
    },
]


def detect_alert_type(message: str) -> str:
    text = message.lower()

    fire_words = ["fire", "smoke", "burn", "flame", "आग", "धुआं", "धुआँ", "जळत", "आग लागली"]
    medical_words = ["medical", "doctor", "ambulance", "blood", "injury", "breathing", "faint", "डॉक्टर", "चोट", "खून", "सांस", "श्वास", "रक्त", "जखम"]
    security_words = ["security", "threat", "attack", "unsafe", "fight", "intruder", "danger", "सुरक्षा", "खतरा", "हमला", "भांडण", "धोका", "हल्ला"]

    if any(word in text for word in fire_words):
        return "fire"
    if any(word in text for word in medical_words):
        return "medical"
    if any(word in text for word in security_words):
        return "security"
    return "other"


def send_panic_alert(alert_type: str, room: str) -> None:
    alert_id = add_alert(
        alert_type=alert_type,
        location=room,
        description=f"{alert_type.title()} panic alert raised from {room}.",
        source="Panic Button",
        room=room,
    )
    st.success(f"Panic alert #{alert_id} sent to admin and {alert_type} staff.")


def render_panic_card(config: dict) -> None:
    st.markdown(
        f"""
        <div class="panic-card" style="background:{config['bg']};border-color:{config['color']}88;color:{config['color']};">
            <div class="panic-ring" style="color:{config['color']};"></div>
            <div class="panic-ring panic-ring-2" style="color:{config['color']};"></div>
            <div class="panic-icon">{config['icon']}</div>
            <div class="panic-title">{config['card_title']}</div>
            <div class="panic-desc">{config['desc']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def app():
    init_session_state()
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown(VOICE_CSS, unsafe_allow_html=True)

    if "guest_room" not in st.session_state:
        st.session_state.guest_room = ROOM_OPTIONS[0]

    page_header(
        "GUEST EMERGENCY REPORT",
        "Select the emergency type, choose the room, and send a voice report that routes to the matching staff team.",
        "🆘",
    )

    st.markdown('<div class="guest-section-label">Select Emergency Type</div>', unsafe_allow_html=True)

    top_left, top_right = st.columns(2, gap="medium")
    bottom_left, bottom_right = st.columns(2, gap="medium")
    card_columns = [top_left, top_right, bottom_left, bottom_right]

    for col, config in zip(card_columns, PANIC_BUTTONS):
        with col:
            render_panic_card(config)
            st.markdown('<div class="panic-button">', unsafe_allow_html=True)
            if st.button(config["button_title"], key=f"panic_{config['type']}", use_container_width=True):
                send_panic_alert(config["type"], st.session_state.get("guest_room", ROOM_OPTIONS[0]))
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="guest-section-label">Room Selection</div>', unsafe_allow_html=True)
    st.selectbox("Select Room", ROOM_OPTIONS, key="guest_room")

    st.markdown('<div class="guest-section-label">Voice Chat</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="voice-box">
            <div class="voice-note">
                Record in English, Hindi, or Marathi. The app will convert the speech to text and send it to the staff group that best matches the emergency.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    audio_note = st.audio_input("Voice Chat")

    if st.button("Send Voice Report", use_container_width=True):
        transcript, status_message = transcribe_audio(audio_note)
        if transcript.strip():
            alert_type = detect_alert_type(transcript)
            alert_id = add_alert(
                alert_type=alert_type,
                location=st.session_state.guest_room,
                description=transcript,
                source="Voice Report",
                room=st.session_state.guest_room,
            )
            st.success(f"Report #{alert_id} sent to admin and {alert_type} staff. {status_message}")
            st.write(f"Transcribed text: {transcript}")
        else:
            st.warning(status_message)


if __name__ == "__main__":
    app()
