# load.py
# Functions to load data

import pandas as pd
from typing import List
from src.schemas import CDR, IPDR

def load_cdr(path: str) -> pd.DataFrame:
    """Load and validate CDR CSV. Returns DataFrame of valid rows."""
    df = pd.read_csv(path)
    valid_rows: List[dict] = []
    bad_rows = 0
    for i, row in df.iterrows():
        try:
            cdr = CDR(**row.to_dict())
            valid_rows.append(cdr.dict())
        except Exception:
            bad_rows += 1
    out = pd.DataFrame(valid_rows)
    print(f"CDR: loaded {len(out)} valid, {bad_rows} dropped")
    print(out.info())
    return out

def load_ipdr(path: str) -> pd.DataFrame:
    """Load and validate IPDR CSV. Returns DataFrame of valid rows."""
    df = pd.read_csv(path)
    valid_rows: List[dict] = []
    bad_rows = 0
    for i, row in df.iterrows():
        try:
            ipdr = IPDR(**row.to_dict())
            valid_rows.append(ipdr.dict())
        except Exception:
            bad_rows += 1
    out = pd.DataFrame(valid_rows)
    print(f"IPDR: loaded {len(out)} valid, {bad_rows} dropped")
    print(out.info())
    return out
