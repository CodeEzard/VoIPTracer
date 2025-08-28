"""Anomaly detection for VoIP call patterns."""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import Tuple, List


def detect_anomalies(df: pd.DataFrame, contamination: float = 0.1) -> pd.DataFrame:
    """Detect anomalous VoIP calls using IsolationForest.
    
    Args:
        df: Call DataFrame with features
        contamination: Expected proportion of anomalies
    
    Returns:
        DataFrame with anomaly scores and labels
    """
    if df.empty or len(df) < 5:
        if not df.empty:
            df['anomaly_score'] = 0.0
            df['is_anomaly'] = False
        return df
    
    # Select features for anomaly detection
    feature_cols = [
        'duration_s',
        'total_pkts',
        'total_bytes',
        'avg_pkt_size',
        'pkts_per_sec',
        'bytes_per_sec',
        'rtp_ratio',
        'sip_ratio',
        'tls_ratio',
        'num_ssrcs',
        'ip_diversity'
    ]
    
    # Filter to available columns
    available_cols = [col for col in feature_cols if col in df.columns]
    
    if not available_cols:
        df['anomaly_score'] = 0.0
        df['is_anomaly'] = False
        return df
    
    # Prepare feature matrix
    X = df[available_cols].fillna(0)
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Fit IsolationForest
    iso_forest = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=100
    )
    
    # Predict anomalies
    labels = iso_forest.fit_predict(X_scaled)
    scores = iso_forest.score_samples(X_scaled)
    
    # Add results to DataFrame
    df = df.copy()
    df['anomaly_score'] = scores
    df['is_anomaly'] = labels == -1
    
    return df


def flag_suspicious_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """Flag specific suspicious patterns in VoIP calls.
    
    Args:
        df: Call DataFrame
    
    Returns:
        DataFrame with additional suspicious pattern flags
    """
    if df.empty:
        return df
    
    df = df.copy()
    
    # Initialize flags
    df['flag_short_burst'] = False
    df['flag_no_rtp'] = False
    df['flag_high_diversity'] = False
    df['flag_unusual_time'] = False
    df['flag_large_packets'] = False
    
    if len(df) == 0:
        return df
    
    # Short duration but many packets (potential scanning/probing)
    if len(df) > 1:  # Only apply if we have multiple calls for comparison
        duration_q75 = df['duration_s'].quantile(0.75)
        pkts_q75 = df['total_pkts'].quantile(0.75)
        df['flag_short_burst'] = (df['duration_s'] < duration_q75 * 0.1) & (df['total_pkts'] > pkts_q75)
    else:
        df['flag_short_burst'] = False
    
    # SIP calls with no RTP (incomplete/failed calls)
    df['flag_no_rtp'] = (df['sip_pkts'] > 0) & (df['rtp_pkts'] == 0) & (df['duration_s'] > 5)
    
    # High IP diversity (potential relay/proxy abuse)
    df['flag_high_diversity'] = df['ip_diversity'] > df['ip_diversity'].quantile(0.95)
    
    # Calls at unusual hours (off-hours activity)
    df['flag_unusual_time'] = (df['hour'] < 6) | (df['hour'] > 23)
    
    # Unusually large packets (potential data exfiltration)
    if 'avg_pkt_size' in df.columns:
        df['flag_large_packets'] = df['avg_pkt_size'] > df['avg_pkt_size'].quantile(0.95)
    
    return df


def summarize_anomalies(df: pd.DataFrame) -> dict:
    """Generate summary statistics for detected anomalies.
    
    Args:
        df: DataFrame with anomaly detection results
    
    Returns:
        Dict with anomaly summary statistics
    """
    if df.empty:
        return {'total_calls': 0, 'anomalies': 0, 'anomaly_rate': 0.0}
    
    total_calls = len(df)
    anomalies = df['is_anomaly'].sum() if 'is_anomaly' in df.columns else 0
    
    summary = {
        'total_calls': total_calls,
        'anomalies': int(anomalies),
        'anomaly_rate': float(anomalies / total_calls) if total_calls > 0 else 0.0
    }
    
    # Add flag summaries if available
    flag_cols = [col for col in df.columns if col.startswith('flag_')]
    for flag_col in flag_cols:
        flag_name = flag_col.replace('flag_', '')
        summary[f'{flag_name}_count'] = int(df[flag_col].sum())
    
    # Top anomalous calls
    if 'anomaly_score' in df.columns and anomalies > 0:
        top_anomalies = df[df['is_anomaly']].nsmallest(5, 'anomaly_score')
        summary['top_anomalies'] = top_anomalies[['call_id', 'anomaly_score', 'duration_s', 'total_pkts']].to_dict('records')
    
    return summary
