# main.py
from core.controller import SecurityController
from spyware_module.integrated_runner import SpywareRunner
from phishing_email_detection.phishing_runner import PhishingRunner
from trojan_detection_and_defense_system.trojan_runner import TrojanRunner
from standalone_malware_detection.malware_runner import MalwareRunner
from usb_threat_detection.usb_runner import USBThreatRunner
from wifi_safety_checker.wifi_runner import WifiSafetyRunner

import warnings
import time
import json
import os

warnings.filterwarnings("ignore")


def calculate_overall_risk(results):
    total_score = sum(r.get("risk_score", 0) for r in results)
    count = len(results)
    return round(total_score / count, 2) if count else 0


def classify_system_risk(score):
    if score <= 30:
        return "SECURE"
    elif score <= 60:
        return "MODERATE RISK"
    elif score <= 80:
        return "HIGH RISK"
    else:
        return "CRITICAL"


def main():
    controller = SecurityController()

    # Register all modules
    modules = [
        SpywareRunner(),
        PhishingRunner(),
        TrojanRunner(),
        MalwareRunner(),
        USBThreatRunner(),
        WifiSafetyRunner()
    ]

    for m in modules:
        controller.register_module(m)

    print("\n========== AI CYBER DEFENCE SYSTEM ==========\n")
    print("Initializing Scan Engine...\n")
    time.sleep(1)

    print("Running security modules...\n")
    all_results = controller.run_all()
    time.sleep(0.5)

    # Save full results including defense decisions for UI
    report = {"modules": all_results}

    overall_score = calculate_overall_risk(all_results)
    system_status = classify_system_risk(overall_score)
    report.update({
        "overall_risk_score": overall_score,
        "system_status": system_status
    })

    os.makedirs("logs", exist_ok=True)
    with open("logs/scan_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("========== MODULE RESULTS ==========\n")
    for idx, r in enumerate(all_results, 1):
        name = r.get("module", "UNKNOWN")
        status = "THREAT" if r.get("threat_detected", False) else "SAFE"
        severity = r.get("severity", "NONE")
        risk = r.get("risk_score", 0)
        action = r.get("action", "N/A")

        # --- FIX: safely handle 'details' which may be dict or list ---
        details = r.get("details", {})
        if isinstance(details, dict):
            decision = details.get("decision", action)
        elif isinstance(details, list) and details:
            # take first dict if possible, else fallback
            decision = details[0].get("decision", action) if isinstance(details[0], dict) else action
        else:
            decision = action

        print(f"[{idx}] {name.upper():20} | Status: {status:6} | "
              f"Severity: {severity:8} | Risk: {risk}/100 | Action: {action}")

        # Print decision details
        if isinstance(decision, dict):
            print(f"  → Decision: {decision.get('recommended_action', action)} | "
                  f"Reason: {decision.get('reason', 'N/A')}")
        elif isinstance(decision, list):
            for d in decision:
                print(f"  → {d}")
        else:
            # simple string fallback
            print(f"  → Decision: {decision}")

    print("\n========== SYSTEM SUMMARY ==========\n")
    print(f"Overall Risk Score : {overall_score}/100")
    print(f"System Security Status : {system_status}")
    print("\nScan report saved to logs/scan_report.json")
    print("\n========== SCAN COMPLETE ==========\n")


if __name__ == "__main__":
    main()