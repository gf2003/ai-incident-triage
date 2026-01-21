import sqlite3

DB_PATH = "data/tickets.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL,
            category TEXT NOT NULL,
            severity TEXT NOT NULL,
            confidence REAL NOT NULL,
            hostname TEXT,
            username TEXT,
            source_ip TEXT,
            summary TEXT NOT NULL,
            raw_event TEXT NOT NULL,
            recommended_actions TEXT NOT NULL
            
        )    
        
        """)
    
    conn.commit()
    conn.close()
    
    