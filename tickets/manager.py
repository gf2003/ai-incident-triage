import sqlite3
from datetime import datetime
from tickets.db import DB_PATH

def create_ticket(
    *, 
    category: str, 
    severity: str, 
    confidence: float, 
    hostname: str, 
    username: str, 
    source_ip: str, 
    summary: str, 
    raw_event: str, 
    recommended_actions: str
    ) -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute(
    """
    INSERT INTO tickets(
        created_at, status, category, severity, confidence, hostname, username, source_ip, summary, raw_event, recommended_actions
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        "OPEN",
        category,
        severity,
        float(confidence),
        hostname or None,
        username or None,
        source_ip or None,
        summary,
        raw_event,
        recommended_actions
    ))
    
    ticket_id = int(cur.lastrowid)
    conn.commit()
    conn.close()
    return ticket_id
