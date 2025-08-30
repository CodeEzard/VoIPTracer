#!/usr/bin/env python3
"""Quick script to test PCAP files for VoIP content."""

import sys
import os
from src.capture import read_pcap

def analyze_pcap(pcap_path):
    """Analyze a PCAP file and show what VoIP content it contains."""
    if not os.path.exists(pcap_path):
        print(f"Error: File {pcap_path} not found")
        return
    
    print(f"Analyzing PCAP file: {pcap_path}")
    print("=" * 50)
    
    packets = list(read_pcap(pcap_path, limit=100))
    
    if not packets:
        print("❌ No VoIP packets detected")
        print("\nThis could mean:")
        print("- The PCAP file doesn't contain VoIP traffic")
        print("- The VoIP traffic uses non-standard ports/protocols")
        print("- The file is corrupted or in an unsupported format")
        return
    
    print(f"✅ Found {len(packets)} VoIP packets")
    
    # Analyze protocols
    protocols = {}
    for pkt in packets:
        proto = pkt['proto']
        protocols[proto] = protocols.get(proto, 0) + 1
    
    print(f"\nProtocols found:")
    for proto, count in sorted(protocols.items()):
        print(f"  {proto}: {count} packets")
    
    # Show sample packets
    print(f"\nSample packets:")
    for i, pkt in enumerate(packets[:5]):
        print(f"  {i+1}. {pkt['proto']} {pkt['src_ip']}:{pkt['src_port']} -> {pkt['dst_ip']}:{pkt['dst_port']}")
        if pkt['call_id']:
            print(f"     Call ID: {pkt['call_id']}")
    
    print(f"\n✅ PCAP file appears to contain valid VoIP traffic!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_pcap.py <pcap_file>")
        print("Example: python test_pcap.py sample.pcap")
        sys.exit(1)
    
    analyze_pcap(sys.argv[1])
