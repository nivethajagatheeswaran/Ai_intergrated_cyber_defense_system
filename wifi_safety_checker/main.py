from .wifi_info import get_wifi_details
from .network_scan import scan_ports
from .heuristics import analyze_wifi
from .packet_analysis import analyze_packets

def run():
    """
    Headless Wi-Fi scan for integration with Orchestrator
    """

    wifi = get_wifi_details()
    suspicious_ips = []
    open_ports = []
    risk_score = 0

    if not wifi or not wifi.get("ssid"):
        # No Wi-Fi connected
        status = "no_wifi"
        action = "allow"

    else:
        # Step 1: Local listening port analysis
        open_ports = scan_ports()

        # Step 2: Environmental risk scoring
        risk_score = analyze_wifi(
            wifi.get("authentication"),
            wifi.get("encryption"),
            open_ports
        )

        # Step 3: Packet-level behavioral sampling
        suspicious_ips = analyze_packets(packet_count=20)

        if suspicious_ips:
            risk_score += 20  # escalate risk if abnormal packet activity detected

        # Step 4: Classify environment risk (not direct malware)
        if risk_score <= 30:
            status = "low_risk_environment"
            action = "allow"
        elif risk_score <= 60:
            status = "moderate_risk_environment"
            action = "human_review"
        else:
            status = "high_risk_environment"
            action = "alert_only"

    # Save structured report
    import os, json
    os.makedirs("wifi_safety_checker/logs", exist_ok=True)

    with open("wifi_safety_checker/logs/scan_report.json", "w") as f:
        json.dump({
            "module": "wifi_safety_checker",
            "wifi_details": wifi,
            "open_ports": open_ports,
            "suspicious_ips": suspicious_ips,
            "risk_score": risk_score,
            "status": status,
            "action": action
        }, f, indent=4)

    return {
        "module": "wifi_safety_checker",
        "wifi_details": wifi,
        "open_ports": open_ports,
        "suspicious_ips": suspicious_ips,
        "risk_score": risk_score,
        "status": status,
        "action": action
    }