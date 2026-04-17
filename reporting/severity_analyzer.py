def analyze_severity(result):

    if not result:
        return "Unknown"

    text = str(result).lower()

    if "vulnerable" in text or "found" in text:
        return "High"

    if "warning" in text:
        return "Medium"

    if "safe" in text or "not vulnerable" in text:
        return "Low"

    return "Info"