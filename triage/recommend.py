import json

ACTIONS = {
    "Authentication" : [
        "Review failed/successful logins for the user and surrounding time window",
        "Check source IP reputation and geolocation",
        "If brute-force suspected: block IP, enforce MFA, and reset credentials.",
    ],
    
    "Privilege": [
        "Validate privileged activity against approved change/request records",
        "Review command history and impacted files",
        "If unauthorized: disable account and escalate to the incident response",
    ],
    
    "Malware": [
        "Isolate host from the network",
        "Quarantine suspicious file and capture hash (SHA-256)",
        "Escalate if repeated scanning or exploitation behavior is observed",
    ],
}

def recommended_actions_json(category: str) -> str:
    actions = ACTIONS.get(category, ["Validate the alert and gather additional context"])
    return json.dumps(actions)