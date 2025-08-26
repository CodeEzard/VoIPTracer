# heuristics.py
# Heuristic algorithms

import yaml
from typing import Optional, Any

# Optionally load allow/deny lists from cfg/rules.yaml (scaffolded)
def load_rules(path: str = "cfg/rules.yaml") -> dict:
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


def is_voip_row(row: dict) -> Optional[str]:
    """Return VoIP flag for a row, or None if not VoIP-related."""
    port = int(row.get("dst_port", -1))
    proto = str(row.get("protocol", "")).upper()
    # SIP signaling
    if port in (5060, 5061):
        return "SIP-Signaling"
    # RTP media
    if 16384 <= port <= 32767:
        return "RTP-Media"
    # OTT VoIP over 443
    if port == 443 and proto in {"UDP", "TCP"}:
        return "App-VoIP-443"
    return None


def add_voip_flags(df):
    """Add a 'voip_flag' column to a DataFrame of IPDR rows."""
    df = df.copy()
    df["voip_flag"] = df.apply(is_voip_row, axis=1)
    return df
