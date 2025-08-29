#!/usr/bin/env python3
"""
PCAP validation and debugging script
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import pyshark
from src.capture import read_pcap, extract_meta

def analyze_pcap(pcap_path: str):
    """Analyze a PCAP file to understand its contents"""
    
    print(f"🔍 Analyzing PCAP file: {pcap_path}")
    print("=" * 60)
    
    if not os.path.exists(pcap_path):
        print(f"❌ File not found: {pcap_path}")
        return
    
    # First, let's see what's actually in the PCAP
    try:
        print("📊 General packet analysis...")
        cap = pyshark.FileCapture(pcap_path)
        
        total_packets = 0
        protocols = {}
        ports = {}
        
        for i, pkt in enumerate(cap):
            if i >= 1000:  # Limit to first 1000 packets
                break
            total_packets += 1
            
            # Count protocols
            if hasattr(pkt, 'highest_layer'):
                protocol = pkt.highest_layer
                protocols[protocol] = protocols.get(protocol, 0) + 1
            
            # Count ports
            if hasattr(pkt, 'tcp'):
                port = f"TCP:{pkt.tcp.dstport}"
                ports[port] = ports.get(port, 0) + 1
            elif hasattr(pkt, 'udp'):
                port = f"UDP:{pkt.udp.dstport}"
                ports[port] = ports.get(port, 0) + 1
        
        cap.close()
        
        print(f"Total packets analyzed: {total_packets}")
        print(f"\nTop protocols found:")
        for proto, count in sorted(protocols.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {proto}: {count}")
        
        print(f"\nTop destination ports:")
        for port, count in sorted(ports.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {port}: {count}")
        
    except Exception as e:
        print(f"❌ Error analyzing PCAP: {e}")
        return
    
    # Now test VoIP extraction
    print(f"\n🎯 VoIP packet extraction test...")
    try:
        voip_packets = list(read_pcap(pcap_path, limit=100))
        print(f"VoIP packets found: {len(voip_packets)}")
        
        if voip_packets:
            print("\nFirst few VoIP packets:")
            for i, pkt in enumerate(voip_packets[:5]):
                print(f"  Packet {i+1}: {pkt['proto']} - {pkt['src_ip']}:{pkt.get('src_port', 'N/A')} -> {pkt['dst_ip']}:{pkt.get('dst_port', 'N/A')}")
                if pkt.get('call_id'):
                    print(f"    Call ID: {pkt['call_id']}")
        else:
            print("❌ No VoIP packets detected with current filters")
            
            # Try alternative detection
            print("\n🔍 Trying alternative detection...")
            try:
                # Look for specific VoIP indicators
                cap = pyshark.FileCapture(pcap_path)
                found_voip_like = []
                
                for i, pkt in enumerate(cap):
                    if i >= 500:  # Check first 500 packets
                        break
                    
                    voip_indicators = []
                    
                    # Check for SIP-like content
                    if hasattr(pkt, 'udp') or hasattr(pkt, 'tcp'):
                        if hasattr(pkt, 'udp'):
                            if int(pkt.udp.dstport) == 5060 or int(pkt.udp.srcport) == 5060:
                                voip_indicators.append("SIP_PORT")
                        if hasattr(pkt, 'tcp'):
                            if int(pkt.tcp.dstport) == 5060 or int(pkt.tcp.srcport) == 5060:
                                voip_indicators.append("SIP_PORT")
                    
                    # Check for RTP-like patterns (UDP, even payload type, etc.)
                    if hasattr(pkt, 'udp'):
                        port = int(pkt.udp.dstport)
                        if 8000 <= port <= 65000 and port % 2 == 0:  # Common RTP port range
                            voip_indicators.append("RTP_LIKE_PORT")
                    
                    if voip_indicators:
                        found_voip_like.append({
                            'packet_num': i,
                            'indicators': voip_indicators,
                            'src': f"{pkt.ip.src if hasattr(pkt, 'ip') else 'N/A'}",
                            'dst': f"{pkt.ip.dst if hasattr(pkt, 'ip') else 'N/A'}",
                            'protocol': pkt.highest_layer if hasattr(pkt, 'highest_layer') else 'Unknown'
                        })
                
                cap.close()
                
                if found_voip_like:
                    print(f"Found {len(found_voip_like)} packets with VoIP-like characteristics:")
                    for pkt in found_voip_like[:10]:
                        print(f"  Packet {pkt['packet_num']}: {pkt['src']} -> {pkt['dst']} ({pkt['protocol']}) - {', '.join(pkt['indicators'])}")
                else:
                    print("❌ No VoIP-like patterns found")
                    
            except Exception as e:
                print(f"❌ Alternative detection failed: {e}")
    
    except Exception as e:
        print(f"❌ VoIP extraction failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pcap_debug.py <path_to_pcap_file>")
        print("Example: python pcap_debug.py sample.pcap")
        sys.exit(1)
    
    pcap_path = sys.argv[1]
    analyze_pcap(pcap_path)
