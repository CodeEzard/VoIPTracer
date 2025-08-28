"""Parse SDP fingerprints and group packets by call/session."""

import re
from typing import Dict, List
from collections import defaultdict


def attach_meta_from_raw_packets(raw_pkts: List[Dict]) -> Dict[str, Dict]:
    """Group packets by call-id/ssrc and extract additional metadata.
    
    Args:
        raw_pkts: List of packet metadata dicts from capture.py
    
    Returns:
        Dict keyed by call_id/ssrc with aggregated call metadata
    """
    calls = defaultdict(lambda: {
        'call_id': '',
        'from_uri': '',
        'to_uri': '',
        'sdp_fp': '',
        'ssrcs': set(),
        'start_ts': float('inf'),
        'end_ts': 0.0,
        'sip_pkts': 0,
        'rtp_pkts': 0,
        'tls_pkts': 0,
        'total_bytes': 0,
        'src_ips': set(),
        'dst_ips': set(),
        'ja3_hashes': set()
    })
    
    for pkt in raw_pkts:
        key = pkt['call_id'] if pkt['call_id'] else f"ssrc_{pkt['ssrc']}"
        call = calls[key]
        
        # Update call metadata
        if pkt['call_id']:
            call['call_id'] = pkt['call_id']
        if pkt['from_uri']:
            call['from_uri'] = pkt['from_uri']
        if pkt['to_uri']:
            call['to_uri'] = pkt['to_uri']
        
        call['ssrcs'].add(pkt['ssrc'])
        call['start_ts'] = min(call['start_ts'], pkt['ts'])
        call['end_ts'] = max(call['end_ts'], pkt['ts'])
        call['total_bytes'] += pkt['pkt_len']
        call['src_ips'].add(pkt['src_ip'])
        call['dst_ips'].add(pkt['dst_ip'])
        
        if pkt['ja3']:
            call['ja3_hashes'].add(pkt['ja3'])
        
        # Count by protocol
        if pkt['proto'] == 'SIP':
            call['sip_pkts'] += 1
            # Extract SDP fingerprint if present
            call['sdp_fp'] = extract_sdp_fingerprint(pkt)
        elif pkt['proto'] == 'RTP':
            call['rtp_pkts'] += 1
        elif pkt['proto'] in ['TLS', 'DTLS']:
            call['tls_pkts'] += 1
    
    # Convert sets to lists for JSON serialization
    result = {}
    for key, call in calls.items():
        call['ssrcs'] = list(call['ssrcs'])
        call['src_ips'] = list(call['src_ips'])
        call['dst_ips'] = list(call['dst_ips'])
        call['ja3_hashes'] = list(call['ja3_hashes'])
        call['duration_s'] = call['end_ts'] - call['start_ts']
        call['total_pkts'] = call['sip_pkts'] + call['rtp_pkts'] + call['tls_pkts']
        result[key] = call
    
    return result


def extract_sdp_fingerprint(pkt: Dict) -> str:
    """Extract a=fingerprint from SDP payload (stub implementation)."""
    # In real implementation, would parse SDP from packet payload
    # For now, return a stub fingerprint
    if pkt['proto'] == 'SIP' and 'INVITE' in pkt.get('from_uri', ''):
        return 'sha-256 AA:BB:CC:DD:EE:FF:00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF:00:11:22:33:44:55:66:77:88:99'
    return ''


def compute_ja3_hash(tls_pkt: Dict) -> str:
    """Compute JA3 hash from TLS handshake (stub implementation)."""
    # Real implementation would extract:
    # - TLS version
    # - Cipher suites
    # - Extensions
    # - Elliptic curves
    # - Point formats
    # Then hash them per JA3 spec
    return f"stub_ja3_{hash(tls_pkt['src_ip'] + tls_pkt['dst_ip']) % 10000:04d}"
