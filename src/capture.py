"""Capture and extract VoIP metadata from pcap files or live traffic."""

import pyshark
from typing import Dict, List, Generator, Optional


def read_pcap(path: str, limit: Optional[int] = None) -> Generator[Dict, None, None]:
    """Read pcap file and yield VoIP metadata dicts.
    
    Args:
        path: Path to pcap file
        limit: Max packets to process (None = all)
    
    Yields:
        Dict with SIP/RTP/TLS metadata
    """
    try:
        cap = pyshark.FileCapture(path, display_filter="sip or rtp or tls or dtls")
    except Exception as e:
        print(f"Error opening pcap file {path}: {e}")
        return
    
    count = 0
    try:
        for pkt in cap:
            if limit and count >= limit:
                break
                
            meta = extract_meta(pkt)
            if meta:
                yield meta
                count += 1
    except Exception as e:
        print(f"Error processing packet {count}: {e}")
    finally:
        cap.close()


def read_live(iface: str = "eth0", limit: Optional[int] = None) -> Generator[Dict, None, None]:
    """Live capture VoIP metadata.
    
    Args:
        iface: Network interface
        limit: Max packets to process
    
    Yields:
        Dict with VoIP metadata
    """
    cap = pyshark.LiveCapture(interface=iface, display_filter="sip or rtp or tls or dtls")
    
    count = 0
    for pkt in cap.sniff_continuously():
        if limit and count >= limit:
            break
            
        meta = extract_meta(pkt)
        if meta:
            yield meta
            count += 1


def extract_meta(pkt) -> Optional[Dict]:
    """Extract metadata from a single packet."""
    meta = {
        'ts': float(pkt.sniff_timestamp) if hasattr(pkt, 'sniff_timestamp') else 0.0,
        'src_ip': pkt.ip.src if hasattr(pkt, 'ip') else '',
        'dst_ip': pkt.ip.dst if hasattr(pkt, 'ip') else '',
        'proto': '',
        'call_id': '',
        'from_uri': '',
        'to_uri': '',
        'ssrc': 0,
        'pkt_len': int(pkt.length),
        'tls_ver': '',
        'ja3': ''
    }
    
    # SIP metadata
    if hasattr(pkt, 'sip'):
        meta['proto'] = 'SIP'
        if hasattr(pkt.sip, 'call_id'):
            meta['call_id'] = str(pkt.sip.call_id)
        if hasattr(pkt.sip, 'from'):
            meta['from_uri'] = str(getattr(pkt.sip, 'from'))
        if hasattr(pkt.sip, 'to'):
            meta['to_uri'] = str(pkt.sip.to)
    
    # RTP metadata
    elif hasattr(pkt, 'rtp'):
        meta['proto'] = 'RTP'
        if hasattr(pkt.rtp, 'ssrc'):
            meta['ssrc'] = int(pkt.rtp.ssrc, 16)
    
    # TLS/DTLS metadata
    elif hasattr(pkt, 'tls'):
        meta['proto'] = 'TLS'
        if hasattr(pkt.tls, 'handshake_version'):
            meta['tls_ver'] = str(pkt.tls.handshake_version)
        # Stub for JA3 - would need raw packet analysis
        meta['ja3'] = 'stub_ja3_hash'
    
    elif hasattr(pkt, 'dtls'):
        meta['proto'] = 'DTLS'
        # Similar DTLS metadata extraction
    
    return meta if meta['proto'] else None
