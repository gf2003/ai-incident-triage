def normalize_severity(sev:str) -> str:
    s = (sev or "").strip().capitalize()
    allowed = {"Low", "Medium", "High", "Critical"}
    return s if s in allowed else "Medium"