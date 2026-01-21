import pandas as pd

REQUIRED_COLUMNS = {"message"}

def read_alerts_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Input file {path} is missing required columns: {sorted(missing)}")
    
    for col in ["hostname", "username", "source_ip"]:
        if col not in df.columns:
            df[col] = ""
    
    df["message"] = df["message"].fillna("").astype(str).str.strip()
    for col in ["hostname", "username", "source_ip"]:
        df[col] = df[col].fillna("").astype(str).str.strip()
    
    return df