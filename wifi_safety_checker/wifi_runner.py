from .main import run as wifi_scan


class WifiSafetyRunner:
        def run(self):
            result = wifi_scan()
            risk = result["risk_score"]
    
            return {
                "module": "wifi_safety_checker",
                "risk_score": risk,
                "environment_risk": True,
                "threat_detected": False,  # WiFi alone is not an attack
                "severity": self._severity(risk),
                "action": result["action"]
            }

        def _severity(self, risk):
            if risk <= 30:
                return "LOW"
            elif risk <= 60:
                return "MEDIUM"
            else:
                return "HIGH"