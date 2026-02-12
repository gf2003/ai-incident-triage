##AI Assisted Incident Triage

## Functions
- Trained simple NLP classifiers (TF+IDF + Logistic Regression) to  predict incident category and severity
- Ingested alerts from CSV
- Auto-Created incident tickets in SQLite
- Wrote tamper-evident audit logs (hash-chained) and provides verification

## Run
```bash
pip -r install requirements.txt
python3 main.py
python audit/verify_audit.py

