import os 
from triage.ingest import read_alerts_csv
from triage.model import train_models, predict
from triage.recommend import recommended_actions_json
from triage.utils import normalize_severity
from tickets.db import init_db
from tickets.manager import create_ticket
from audit.audit_logger import write_audit

def ensure_dirs():
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/models", exist_ok=True)

def run(alerts_csv: str):
    ensure_dirs()
    init_db()
    df = read_alerts_csv(alerts_csv)
    
    write_audit("pipeline_started", "system", None, {"source": alerts_csv, "count": int(len(df))})
    
    for _, row in df.iterrows():
        msg = str(row["message"]).strip()
        if not msg:
            continue
        category, severity, conf = predict(msg)
        severity = normalize_severity(severity)
        
        actions = recommended_actions_json(category)
        
        summary = f"{category} triaged as {severity} (conf={conf:.2f})"
        ticket_id = create_ticket(
            category=category,
            severity=severity,
            confidence=conf,
            hostname=row.get("hostname"),
            username=row.get("username"),
            source_ip=row.get("source_ip"),
            summary=summary,
            raw_event=msg,
            recommended_actions=actions
        )
        
        write_audit("ticket_created", "system", ticket_id, {
            "category": category,
            "severity": severity,
            "confidence": conf
        })
        
    write_audit("pipeline_finished", "system", None, {"source": alerts_csv})
        
def main():
    ensure_dirs()
    train_models("samples/labeled_training.csv")
    run("samples/alerts.csv")
    print("Done. Tickets created and audit log written.")
    print("Verify audit with: python audit/verify_audit.py")

if __name__ == "__main__":
    main()