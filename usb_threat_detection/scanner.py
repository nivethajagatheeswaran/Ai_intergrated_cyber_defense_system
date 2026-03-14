import os
from .utils import calculate_hash, calculate_entropy
from .heuristics import heuristic_analysis
from .risk_engine import classify_risk

def scan_usb(path):
    report = []

    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                with open(file_path, "rb") as f:
                    data = f.read(2048)

                entropy = calculate_entropy(data)
                size = os.path.getsize(file_path)
                score = heuristic_analysis(file, size, entropy)
                risk = classify_risk(score)
                file_hash = calculate_hash(file_path)

                if risk != "LOW RISK":
                    report.append({
                        "file": file_path,
                        "risk": risk,
                        "score": score,
                        "hash": file_hash
                    })

            except:
                pass

    return report
