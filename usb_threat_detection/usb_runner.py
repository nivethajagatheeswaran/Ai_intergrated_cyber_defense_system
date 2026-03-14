from .main import run as usb_scan


class USBThreatRunner:
    def run(self):
        result = usb_scan()
        risk = result["risk_score"]

        return {
            "module": "usb_threat_detection",
            "risk_score": risk,
            "threat_detected": risk > 50,
            "severity": self._severity(risk),
            "action": result["action"]
        }

    def _severity(self, risk):
        if risk <= 50:
            return "LOW"
        elif risk <= 80:
            return "MEDIUM"
        else:
            return "CRITICAL"