# Simplified imports for serverless environment
import os
import sys
import tempfile
import subprocess
import json
from typing import List, Dict, Any

def read_pcap_simple(pcap_path: str, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Simplified PCAP reading for serverless environments.
    Uses tshark directly instead of pyshark to avoid asyncio issues.
    """
    try:
        # Use tshark to extract basic packet info
        cmd = [
            'tshark', '-r', pcap_path, '-T', 'json', '-c', str(limit),
            '-Y', 'sip or rtp or rtcp',
            '-e', 'frame.number',
            '-e', 'frame.time',
            '-e', 'ip.src',
            '-e', 'ip.dst', 
            '-e', 'udp.srcport',
            '-e', 'udp.dstport',
            '-e', 'sip.Call-ID',
            '-e', 'sip.From',
            '-e', 'sip.To',
            '-e', 'sip.Method',
            '-e', 'rtp.ssrc'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            print(f"tshark error: {result.stderr}")
            return []
        
        try:
            packets = json.loads(result.stdout)
            return packets if isinstance(packets, list) else []
        except json.JSONDecodeError:
            return []
            
    except Exception as e:
        print(f"Error reading PCAP: {e}")
        return []

def extract_simple_calls(packets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Extract call information from packets for serverless environment.
    """
    calls = {}
    
    for packet in packets:
        try:
            layers = packet.get('_source', {}).get('layers', {})
            
            # Look for SIP packets
            if 'sip' in layers:
                sip = layers['sip']
                call_id = sip.get('sip.Call-ID', ['unknown'])[0] if isinstance(sip.get('sip.Call-ID'), list) else sip.get('sip.Call-ID', 'unknown')
                
                if call_id not in calls:
                    calls[call_id] = {
                        'call_id': call_id,
                        'from_uri': sip.get('sip.From', ['unknown'])[0] if isinstance(sip.get('sip.From'), list) else sip.get('sip.From', 'unknown'),
                        'to_uri': sip.get('sip.To', ['unknown'])[0] if isinstance(sip.get('sip.To'), list) else sip.get('sip.To', 'unknown'),
                        'packets': 0,
                        'duration': 0.0,
                        'anomaly': False
                    }
                
                calls[call_id]['packets'] += 1
                
        except Exception as e:
            continue
    
    return list(calls.values())
