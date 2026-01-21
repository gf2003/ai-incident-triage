import hashlib
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT_PATH = os.path.join(BASE_DIR, "data", "audit.log")


def verify():
    prev = "GENESIS"
    try:
        with open(AUDIT_PATH, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, start=1):
                entry = json.loads(line)
                entry_hash = entry.pop("entry_hash")
                
                if entry.get("prev_hash") != prev:
                    return False, f"Chain broken at line {i}: prev_hash mismatch"
                
                prev = entry_hash
        return True, "Audit Log Ok"
    except FileNotFoundError:
        return True, "No audit.log found (nothing to verify)"

if __name__ == "__main__":
    ok, msg = verify()
    print(msg)