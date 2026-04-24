# 🛡️ CrisisGuard — Rapid Emergency Response Platform

> Accelerated Emergency Response and Crisis Coordination for Hospitality Venues

---

## 📁 Folder Structure

```
rapid_crisis_response/
├── app.py                          # Main entry point (Home screen)
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── config.toml                 # Streamlit dark theme configuration
├── pages/
│   ├── 1_👤_Guest_SOS.py           # Guest SOS portal (4 panic buttons + voice)
│   ├── 2_👷_Staff_Dashboard.py     # Staff alert dashboard with status controls
│   └── 3_🎛️_Admin_Dashboard.py    # Admin analytics + team assignments
└── utils/
    ├── __init__.py
    ├── state.py                    # Shared session state & alert management
    └── styles.py                   # Global CSS + UI helper functions
```

---

## 🚀 Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
cd rapid_crisis_response
streamlit run app.py
```

---

## 📱 Pages Overview

### 👤 Guest SOS Portal
- **4 SOS Panic Buttons**: Fire 🔥 | Medical 🏥 | Security 🔒 | Other ⚠️
- Each button triggers a room/location form before dispatching the alert
- **Voice Emergency Report**: Select language (English / Hindi / Marathi), type or dictate message
- Sidebar shows live emergency contacts (Police 100, Ambulance 108, Fire 101, etc.)

### 👷 Staff Operations Dashboard
- Real-time **Emergency Alert Feed** with automatic updates
- Filter by: Status | Emergency Type | Source (SOS / Voice)
- Every alert card shows: type badge, voice/SOS badge, status pill, location, timestamp
- **3-action buttons** per alert: ✅ Resolved | 🕐 Pending | 🔄 In Progress
- Live summary counts in sidebar

### 🎛️ Admin Control Center
- **KPI Strip**: Total, Fire, Medical, Security, Other counts
- **Status Row**: Pending / In Progress / Resolved with percentages
- **4 Analytics Charts**:
  1. Emergency Type Bar Chart
  2. Status Breakdown Donut
  3. Hourly Activity Line Chart (Last 12h)
  4. Alert Source Split (SOS vs Voice)
- **4 Staff Assignment Boxes**: Fire / Medical / Security / Other teams (5 members each)
  - Active emergency boxes glow and pulse in alert color
- **Emergency Contact Directory**: Police, Ambulance, Fire, Women Helpline, Disaster Mgmt, Hotel Security, Maintenance
- **Recent Alert Log Table**: Last 10 alerts with full details

---

## ⚙️ Tech Stack
- **Streamlit** — Multi-page app framework
- **Plotly** — Interactive charts
- **Session State** — In-memory alert store (no DB needed for demo)

---

## 🎨 Design System
- **Font**: Rajdhani (headers) + DM Sans (body) + JetBrains Mono (codes)
- **Theme**: Dark tactical UI (`#0a0c10` base)
- **Accent colors**: Blue `#00a8ff` | Red `#ff3b3b` | Green `#00e676` | Yellow `#ffd600`
- **Emergency colors**: Fire `#ff4500` | Medical `#00bcd4` | Security `#7c4dff` | Other `#ff9800`
