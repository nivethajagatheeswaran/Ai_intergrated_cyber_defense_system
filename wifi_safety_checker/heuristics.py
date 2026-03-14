def analyze_wifi(auth_type, encryption, open_ports):
    score = 0

    # Authentication risk (environmental risk, not attack)
    if auth_type in ["Open", "None"]:
        score += 25
    elif "WPA" in str(auth_type):
        score += 5

    # Encryption strength
    if encryption in ["None"]:
        score += 30
    elif encryption in ["WEP"]:
        score += 20
    elif "WPA" in str(encryption):
        score += 5

    # Suspicious outbound open ports (mild indicator)
    if len(open_ports) > 0:
        score += 10

    return score