#!/usr/bin/env python3
"""
VoIP PCAP Generator
Creates synthetic VoIP traffic for testing VoIP analysis tools
"""

import os
import sys
import time
import random
from scapy.all import *
from scapy.layers.inet import IP, UDP, TCP
from scapy.layers.rtp import RTP

def generate_sip_invite(src_ip, dst_ip, call_id, from_uri, to_uri):
    """Generate a SIP INVITE packet"""
    sip_invite = f"""INVITE {to_uri} SIP/2.0
Via: SIP/2.0/UDP {src_ip}:5060;branch=z9hG4bK1234567890
Max-Forwards: 70
To: <{to_uri}>
From: <{from_uri}>;tag=12345
Call-ID: {call_id}
CSeq: 1 INVITE
Contact: <sip:{src_ip}:5060>
Content-Type: application/sdp
Content-Length: 200

v=0
o=user 123456 654321 IN IP4 {src_ip}
s=-
c=IN IP4 {src_ip}
t=0 0
m=audio 8000 RTP/AVP 0
a=rtpmap:0 PCMU/8000"""
    
    return IP(src=src_ip, dst=dst_ip) / UDP(sport=5060, dport=5060) / Raw(load=sip_invite)

def generate_sip_200_ok(src_ip, dst_ip, call_id, from_uri, to_uri):
    """Generate a SIP 200 OK response"""
    sip_200 = f"""SIP/2.0 200 OK
Via: SIP/2.0/UDP {dst_ip}:5060;branch=z9hG4bK1234567890
To: <{to_uri}>;tag=54321
From: <{from_uri}>;tag=12345
Call-ID: {call_id}
CSeq: 1 INVITE
Contact: <sip:{src_ip}:5060>
Content-Type: application/sdp
Content-Length: 180

v=0
o=user 654321 123456 IN IP4 {src_ip}
s=-
c=IN IP4 {src_ip}
t=0 0
m=audio 8001 RTP/AVP 0
a=rtpmap:0 PCMU/8000"""
    
    return IP(src=src_ip, dst=dst_ip) / UDP(sport=5060, dport=5060) / Raw(load=sip_200)

def generate_rtp_packet(src_ip, dst_ip, src_port, dst_port, ssrc, seq_num):
    """Generate an RTP packet"""
    # Simple RTP header (version=2, padding=0, extension=0, cc=0, marker=0, pt=0)
    rtp_header = struct.pack('!BBHII', 0x80, 0x00, seq_num, int(time.time()), ssrc)
    # Add some dummy audio payload (20 bytes of silence)
    audio_payload = b'\x00' * 20
    
    return IP(src=src_ip, dst=dst_ip) / UDP(sport=src_port, dport=dst_port) / Raw(load=rtp_header + audio_payload)

def generate_voip_pcap(filename="sample_voip.pcap", num_calls=3):
    """Generate a complete VoIP PCAP file with multiple calls"""
    
    print(f"🎯 Generating VoIP PCAP file: {filename}")
    print(f"📞 Number of calls: {num_calls}")
    
    packets = []
    timestamp = time.time()
    
    # Define some sample IP addresses and phone numbers
    scenarios = [
        {
            "src_ip": "192.168.1.100",
            "dst_ip": "192.168.1.200", 
            "from_uri": "sip:alice@company.com",
            "to_uri": "sip:bob@company.com",
            "type": "normal"
        },
        {
            "src_ip": "10.0.1.50",
            "dst_ip": "203.0.113.10",
            "from_uri": "sip:attacker@malicious.com", 
            "to_uri": "sip:victim@target.com",
            "type": "suspicious"
        },
        {
            "src_ip": "172.16.0.10",
            "dst_ip": "172.16.0.20",
            "from_uri": "sip:user1@office.local",
            "to_uri": "sip:user2@office.local", 
            "type": "internal"
        }
    ]
    
    for call_num in range(num_calls):
        scenario = scenarios[call_num % len(scenarios)]
        call_id = f"call-{call_num+1}@{scenario['src_ip']}"
        
        print(f"  📱 Generating Call {call_num+1}: {scenario['from_uri']} -> {scenario['to_uri']}")
        
        # 1. SIP INVITE
        invite_pkt = generate_sip_invite(
            scenario['src_ip'], scenario['dst_ip'], 
            call_id, scenario['from_uri'], scenario['to_uri']
        )
        invite_pkt.time = timestamp
        packets.append(invite_pkt)
        timestamp += random.uniform(0.1, 0.5)
        
        # 2. SIP 200 OK (after some delay)
        ok_pkt = generate_sip_200_ok(
            scenario['dst_ip'], scenario['src_ip'],
            call_id, scenario['from_uri'], scenario['to_uri'] 
        )
        ok_pkt.time = timestamp
        packets.append(ok_pkt)
        timestamp += random.uniform(0.1, 0.3)
        
        # 3. Generate RTP stream (bidirectional)
        ssrc1 = random.randint(1000000, 9999999)
        ssrc2 = random.randint(1000000, 9999999)
        
        # Generate some RTP packets for this call
        rtp_duration = random.uniform(5, 30)  # 5-30 second calls
        rtp_packets = int(rtp_duration * 50)  # 50 packets per second (20ms intervals)
        
        for i in range(rtp_packets):
            # RTP from caller to callee
            rtp1 = generate_rtp_packet(
                scenario['src_ip'], scenario['dst_ip'],
                8000 + call_num*2, 8001 + call_num*2,
                ssrc1, i
            )
            rtp1.time = timestamp
            packets.append(rtp1)
            
            # RTP from callee to caller  
            rtp2 = generate_rtp_packet(
                scenario['dst_ip'], scenario['src_ip'],
                8001 + call_num*2, 8000 + call_num*2,
                ssrc2, i
            )
            rtp2.time = timestamp + 0.01
            packets.append(rtp2)
            
            timestamp += 0.02  # 20ms between RTP packets
        
        # Add some anomalous behavior for suspicious calls
        if scenario['type'] == 'suspicious':
            # Generate rapid successive calls (scanning behavior)
            for burst in range(5):
                burst_call_id = f"scan-{call_num}-{burst}@{scenario['src_ip']}"
                rapid_invite = generate_sip_invite(
                    scenario['src_ip'], f"203.0.113.{10+burst}",
                    burst_call_id, scenario['from_uri'], f"sip:target{burst}@victim.com"
                )
                rapid_invite.time = timestamp
                packets.append(rapid_invite)
                timestamp += 0.1  # Very rapid calls
        
        timestamp += random.uniform(1, 5)  # Gap between calls
    
    # Write PCAP file
    print(f"💾 Writing {len(packets)} packets to {filename}")
    wrpcap(filename, packets)
    
    # Verify file was created
    if os.path.exists(filename):
        file_size = os.path.getsize(filename)
        print(f"✅ PCAP file created successfully!")
        print(f"   📁 File: {filename}")
        print(f"   📊 Size: {file_size} bytes")
        print(f"   📦 Packets: {len(packets)}")
    else:
        print(f"❌ Failed to create PCAP file")

def main():
    """Main function"""
    print("🎙️  VoIP PCAP Generator")
    print("=" * 50)
    
    # Check if scapy is available
    try:
        from scapy.all import wrpcap
    except ImportError:
        print("❌ Scapy is required but not installed")
        print("Install with: pip install scapy")
        sys.exit(1)
    
    # Generate the PCAP
    filename = "sample_voip_traffic.pcap"
    num_calls = 5
    
    generate_voip_pcap(filename, num_calls)
    
    print(f"\n🎉 VoIP PCAP generation complete!")
    print(f"You can now test with: python pcap_debug.py {filename}")

if __name__ == "__main__":
    main()
