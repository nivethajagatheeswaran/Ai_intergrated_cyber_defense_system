from .scanner import scan_usb
import os
import json

def run(path="E:/"):  # default path or can be passed by orchestrator
    """
    Headless USB scan for integration with Orchestrator
    """
    results = scan_usb(path)

    # Calculate max risk among files
    if results:
        risk_score = max(r["score"] for r in results)
    else:
        risk_score = 0

    # Determine action based on thresholds
    if risk_score <= 50:
        status = "safe"
        action = "allow"
    elif risk_score <= 80:
        status = "suspicious"
        action = "human_in_loop"
    else:
        status = "malicious"
        action = "auto_quarantine"

    # Optional: save report for logs
    os.makedirs("usb_threat_detection/logs", exist_ok=True)
    with open("usb_threat_detection/logs/scan_report.json", "w") as f:
        json.dump({
            "module": "usb_threat_detection",
            "risk_score": risk_score,
            "status": status,
            "action": action,
            "files_scanned": len(results)
        }, f, indent=4)

    return {
        "module": "usb_threat_detection",
        "risk_score": risk_score,
        "status": status,
        "action": action
    }