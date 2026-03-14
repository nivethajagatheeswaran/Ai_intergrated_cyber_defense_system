SUSPICIOUS_EXTENSIONS = [
    ".exe", ".dll", ".scr", ".bat", ".ps1", ".vbs"
]

def heuristic_analysis(file_name, file_size, entropy):
    score = 0

    if any(file_name.lower().endswith(ext) for ext in SUSPICIOUS_EXTENSIONS):
        score += 30

    if file_size > 10 * 1024 * 1024:
        score += 20

    if entropy > 7.2:
        score += 40

    return score
