"""Aggregate call metadata into pandas DataFrame."""

import pandas as pd
from typing import Dict, List


def calls_to_dataframe(calls: Dict[str, Dict]) -> pd.DataFrame:
    """Convert call metadata dict to pandas DataFrame.
    
    Args:
        calls: Dict from parser.attach_meta_from_raw_packets()
    
    Returns:
        DataFrame with one row per call/session
    """
    rows = []
    
    for call_id, meta in calls.items():
        row = {
            'call_id': call_id,
            'from_uri': meta['from_uri'],
            'to_uri': meta['to_uri'],
            'start_ts': meta['start_ts'],
            'end_ts': meta['end_ts'],
            'duration_s': meta['duration_s'],
            'total_pkts': meta['total_pkts'],
            'sip_pkts': meta['sip_pkts'],
            'rtp_pkts': meta['rtp_pkts'],
            'tls_pkts': meta['tls_pkts'],
            'total_bytes': meta['total_bytes'],
            'avg_pkt_size': meta['total_bytes'] / max(meta['total_pkts'], 1),
            'num_ssrcs': len(meta['ssrcs']),
            'num_src_ips': len(meta['src_ips']),
            'num_dst_ips': len(meta['dst_ips']),
            'has_sdp_fp': bool(meta['sdp_fp']),
            'num_ja3': len(meta['ja3_hashes']),
            'sdp_fp': meta['sdp_fp'],
            'ja3_list': ','.join(meta['ja3_hashes']),
            'src_ips': ','.join(meta['src_ips']),
            'dst_ips': ','.join(meta['dst_ips'])
        }
        rows.append(row)
    
    df = pd.DataFrame(rows)
    
    # Convert timestamps to datetime
    if not df.empty:
        df['start_dt'] = pd.to_datetime(df['start_ts'], unit='s')
        df['end_dt'] = pd.to_datetime(df['end_ts'], unit='s')
    
    return df


def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived features for anomaly detection.
    
    Args:
        df: DataFrame from calls_to_dataframe()
    
    Returns:
        DataFrame with additional feature columns
    """
    if df.empty:
        return df
    
    df = df.copy()
    
    # Rate features
    df['pkts_per_sec'] = df['total_pkts'] / df['duration_s'].clip(lower=0.001)
    df['bytes_per_sec'] = df['total_bytes'] / df['duration_s'].clip(lower=0.001)
    
    # Ratio features
    df['rtp_ratio'] = df['rtp_pkts'] / df['total_pkts'].clip(lower=1)
    df['sip_ratio'] = df['sip_pkts'] / df['total_pkts'].clip(lower=1)
    df['tls_ratio'] = df['tls_pkts'] / df['total_pkts'].clip(lower=1)
    
    # Call complexity
    df['ip_diversity'] = df['num_src_ips'] + df['num_dst_ips']
    df['ssrc_diversity'] = df['num_ssrcs']
    
    # Temporal features
    df['hour'] = df['start_dt'].dt.hour
    df['day_of_week'] = df['start_dt'].dt.dayofweek
    
    return df


def filter_calls(df: pd.DataFrame, min_duration: float = 0.1, min_pkts: int = 5) -> pd.DataFrame:
    """Filter out very short/small calls that are likely not real VoIP sessions.
    
    Args:
        df: Call DataFrame
        min_duration: Minimum duration in seconds
        min_pkts: Minimum packet count
    
    Returns:
        Filtered DataFrame
    """
    if df.empty:
        return df
    
    mask = (df['duration_s'] >= min_duration) & (df['total_pkts'] >= min_pkts)
    return df[mask].reset_index(drop=True)
