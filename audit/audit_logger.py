import hashlib
import json
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT_PATH = os.path.join(BASE_DIR, "data", "audit.log")

def _last_hash() -> str:
    try:
        with open(AUDIT_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                return "GENESIS"
            return json.loads(lines[-1])["entry_hash"]
    except FileNotFoundError:
        return "GENESIS"
    
def write_audit(actions: str, actor: str, ticket_id, details: dict):
    prev = _last_hash()
    
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": actions,
        "actor": actor,
        "ticket_id": ticket_id,
        "details": details, 
        "prev_hash": prev
    }
    raw = json.dumps(entry, sort_keys=True).encode("utf-8")
    entry["entry_hash"] = hashlib.sha256(raw).hexdigest()
    
    with open(AUDIT_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
        