import subprocess

def get_wifi_details():
    try:
        result = subprocess.check_output(
            ["netsh", "wlan", "show", "interfaces"],
            shell=True,
            text=True
        )

        details = {
            "ssid": None,
            "authentication": None,
            "encryption": None
        }

        for line in result.split("\n"):
            if "SSID" in line and "BSSID" not in line:
                details["ssid"] = line.split(":")[1].strip()
            elif "Authentication" in line:
                details["authentication"] = line.split(":")[1].strip()
            elif "Cipher" in line:
                details["encryption"] = line.split(":")[1].strip()

        return details
    except:
        return None
