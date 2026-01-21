#AI Assisted Incident Triage

## Functions
- Trains simple NLP classifiers (TF+IDF + Logistic Regression) to  predict incident category and severity
- Ingest alerts from CSV
- Auto-Creates incident tickets in SQLite
- Writes tamper-evident audit logs (hash-chained) and provides verification

## Run
```bash
pip -r install requirements.txt
python3 main.py
python audit/verify_audit.py

