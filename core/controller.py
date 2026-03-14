# core/controller.py
def human_decision_loop(module_name, threat_details, recommended_action):
    """
    Simulate human-in-loop decision for demo with max 2 attempts
    """
    attempts = 0
    max_attempts = 2

    while attempts < max_attempts:
        print(f"\n[{module_name.upper()}] Threat detected!")
        print(f"Recommended action: {recommended_action}")
        decision = input("Type 'ALLOW' to allow, 'QUARANTINE' to quarantine: ").strip().upper()

        if decision == "QUARANTINE":
            print(f"✅ Action applied: {module_name} quarantined.\n")
            break
        elif decision == "ALLOW":
            print(f"⚠ You chose to allow the process. Showing threat details:")
            for k, v in threat_details.items():
                print(f"  {k}: {v}")
            attempts += 1
            if attempts < max_attempts:
                print("\nYou must decide again whether to ALLOW or QUARANTINE.\n")
            else:
                print("\nMaximum attempts reached. Auto applying QUARANTINE for safety.\n")
                break
        else:
            print("Invalid input. Please type ALLOW or QUARANTINE.")
            
class SecurityController:
    def __init__(self):
        self.modules = []

    def register_module(self, module):
        self.modules.append(module)


    def run_all(self):
        results = []
        for module in self.modules:
            print(f"[+] Running {module.__class__.__name__}")
            result = module.run()
            results.append(result)
        
            if not result["threat_detected"]:
                print(f"  ✅ Module SAFE. No action required.\n")
            else:
                print(f"  ⚠ Module detected threat! Severity: {result['severity']}")
        
                # Trojan / Spyware example
                if result["module"] in ["trojan", "spyware"]:
                    # recommended_action comes from module.run()
                    recommended_action = result.get("decision", {}).get("recommended_action", "QUARANTINE")
                    threat_details = result.get("details", {})
                    if recommended_action == "AUTO":
                        print(f"  🔒 Auto action applied: QUARANTINE\n")
                    else:
                        # Human-in-loop demo
                        human_decision_loop(result["module"], threat_details, recommended_action)
        
                # Phishing emails
                elif result["module"] == "phishing":
                    for email in result["details"]:
                        print(f"  ⚠ Phishing email detected: {email['email']}")
                        print(f"    → Recommended action: QUARANTINE / USER REVIEW")

        return results 
    