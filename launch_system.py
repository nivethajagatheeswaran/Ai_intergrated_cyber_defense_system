import subprocess
import webbrowser
import time
import splash_screen

print("Launching AI Cyber Defence System...")

# Start Streamlit
subprocess.Popen(["streamlit", "run", "ui.py"])

time.sleep(3)

webbrowser.open("http://localhost:8501")

print("Dashboard started.")