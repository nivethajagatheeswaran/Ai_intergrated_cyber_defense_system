import streamlit as st
import json
import os
import subprocess
import time
import pandas as pd

# -----------------------------
# Quarantine Setup
# -----------------------------
QUARANTINE_FOLDER = "quarantine"

if not os.path.exists(QUARANTINE_FOLDER):
    os.makedirs(QUARANTINE_FOLDER)


import re

def sanitize_filename(name):
    # remove illegal characters for Windows
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    name = name.replace("@", "_")
    name = name.replace(" ", "_")
    return name


def quarantine_email(email_data):

    sender = email_data.get("sender", "unknown")
    safe_sender = sanitize_filename(sender)

    filename = os.path.join(
        QUARANTINE_FOLDER,
        f"{safe_sender}_{int(time.time())}.json"
    )

    with open(filename, "w") as f:
        json.dump(email_data, f, indent=4)

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(
    page_title="AI Cyber Defence System",
    page_icon="🛡",
    layout="wide"
)

st.title("🛡 AI Cyber Defence System")
st.markdown("### Enterprise Security Monitoring Console")

REPORT_PATH = "logs/scan_report.json"

if "scan_completed" not in st.session_state:
    st.session_state.scan_completed = False

if "review_email" not in st.session_state:
    st.session_state.review_email = None

if "wifi_warning" not in st.session_state:
    st.session_state.wifi_warning = False


# -----------------------------
# Scan Controls
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Run Full System Scan", use_container_width=True):
        with st.spinner("Running Security Modules..."):
            subprocess.run(["python", "main.py"])
            time.sleep(1)
        st.session_state.scan_completed = True
        st.success("✅ Scan Completed Successfully!")
        st.rerun()

with col2:
    if st.button("🔄 Rescan System", use_container_width=True):
        with st.spinner("Re-running Security Scan..."):
            subprocess.run(["python", "main.py"])
            time.sleep(1)
        st.success("✅ Rescan Completed!")
        st.rerun()

if not st.session_state.scan_completed:
    st.stop()


# -----------------------------
# Load Scan Report
# -----------------------------
if not os.path.exists(REPORT_PATH):
    st.error("Scan report not found.")
    st.stop()

with open(REPORT_PATH, "r") as f:
    data = json.load(f)

modules = data.get("modules", [])
if not modules:
    st.warning("No module data found.")
    st.stop()

overall_risk = data.get("overall_risk_score", 0)
system_status = data.get("system_status", "UNKNOWN")
threat_detected = any(m.get("threat_detected", False) for m in modules)


# -----------------------------
# Dashboard Overview
# -----------------------------
st.markdown("## 📊 System Overview")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Overall Risk Score", f"{overall_risk}/100")

with col2:
    if threat_detected:
        st.error("⚠ Threat Detected")
    else:
        st.success("✅ System Secure")

with col3:
    st.metric("Active Modules", len(modules))

st.divider()

# -----------------------------
# Threat Intelligence Panel
# -----------------------------
st.markdown("## 🧠 Threat Intelligence")

threat_count = sum(1 for m in modules if m.get("threat_detected"))
safe_count = len(modules) - threat_count

col1, col2, col3 = st.columns(3)

with col1:
    st.success(f"🟢 Safe Modules\n\n{safe_count}")

with col2:
    st.error(f"🔴 Threat Modules\n\n{threat_count}")

with col3:
    st.info(f"🧩 Total Modules\n\n{len(modules)}")

st.divider()

# -----------------------------
# Module Details
# -----------------------------
st.markdown("## 🧩 Module Status")

for module in modules:

    name = module.get("module", "UNKNOWN").upper()
    risk = module.get("risk_score", 0)
    severity = module.get("severity", "NONE")
    if module.get("threat_detected"):
        status = "🔴 THREAT"
    else:
        status = "🟢 SAFE"
    action = module.get("action", "NONE")
    details = module.get("details", {})

    with st.container():

        colA, colB = st.columns([3, 2])

        with colA:

            st.markdown(f"### {name}")
            st.write(f"**Status:** {status}")
            st.write(f"**Severity:** {severity}")
            st.write(f"**Recommended Action:** {action}")

            # -----------------------------
            # PHISHING MODULE REVIEW
            # -----------------------------
            if name == "PHISHING" and action == "USER_REVIEW":

                if isinstance(details, list):

                    for idx, threat in enumerate(details):

                        if st.button(f"👁 Review Email {idx+1}", key=f"review_{idx}"):

                            st.session_state.review_email = threat


            # -----------------------------
            # WIFI WARNING
            # -----------------------------
            if name == "WIFI_SAFETY_CHECKER" and severity == "HIGH":

                if st.button("⚠ View WiFi Warning"):

                    st.session_state.wifi_warning = True


        with colB:

            st.write("Risk Level")
            st.progress(int(risk))
            if risk <= 30:
                st.success("Low Risk")
            elif risk <= 60:
                st.warning("Moderate Risk")
            else:
                st.error("High Risk")
            st.write(f"{risk}/100")

        st.divider()


# -----------------------------
# PHISHING REVIEW POPUP
# -----------------------------
if st.session_state.review_email:

    threat = st.session_state.review_email

    st.warning("⚠ Potential Phishing Email Detected")

    st.write(f"**Sender:** {threat['sender']}")
    st.write(f"**Subject:** {threat['email']}")
    st.write(f"**Confidence:** {threat['score']}%")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("✅ Allow Email"):

            st.success("Email allowed by user.")
            st.session_state.review_email = None


    with col2:

        if st.button("🛑 Quarantine Email"):

            quarantine_email(threat)
            st.warning("Email moved to quarantine folder.")
            st.session_state.review_email = None


# -----------------------------
# WIFI WARNING POPUP
# -----------------------------
if st.session_state.wifi_warning:

    st.error("⚠ Unsafe WiFi Network Detected")

    st.write("Your current WiFi network may be insecure.")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Allow Connection"):

            st.success("User accepted the risk.")
            st.session_state.wifi_warning = False


    with col2:

        if st.button("Turn Off WiFi"):

            try:

                subprocess.run(
                    ['netsh', 'interface', 'set', 'interface', 'Wi-Fi', 'disable'],
                    shell=True
                )

                st.warning("WiFi turned off for safety.")

            except:

                st.error("Failed to disable WiFi.")

            st.session_state.wifi_warning = False


# -----------------------------
# Risk Distribution Chart
# -----------------------------
st.markdown("## 📈 Risk Distribution")

df = pd.DataFrame({
    "Module": [m.get("module", "UNKNOWN").upper() for m in modules],
    "Risk Score": [m.get("risk_score", 0) for m in modules]
})

st.bar_chart(df.set_index("Module"))

st.markdown("---")
st.caption("AI-Based Cyber Defence Monitoring System | Live Scan Engine")

# -----------------------------
# Quarantine Center
# -----------------------------
st.markdown("## 📥 Quarantine Center")

files = os.listdir(QUARANTINE_FOLDER)

if not files:
    st.success("No emails in quarantine.")
else:

    for file in files:

        path = os.path.join(QUARANTINE_FOLDER, file)

        with open(path) as f:
            email_data = json.load(f)

        with st.expander(f"📧 {email_data['email']}"):

            st.write("Sender:", email_data["sender"])
            st.write("Confidence:", email_data["score"])

            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Restore Email {file}"):

                    os.remove(path)
                    st.success("Email restored.")
                    st.rerun()

            with col2:
                if st.button(f"Delete Email {file}"):

                    os.remove(path)
                    st.warning("Email deleted permanently.")
                    st.rerun()