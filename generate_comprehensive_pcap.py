#!/usr/bin/env python3
"""Generate a comprehensive VoIP PCAP file with various scenarios."""

import time
import random
from scapy.all import *

def generate_comprehensive_voip_pcap(filename="comprehensive_voip_traffic.pcap", num_calls=5):
    """Generate a comprehensive PCAP file with various VoIP scenarios."""
    
    packets = []
    call_counter = 1
    current_time = time.time()
    
    print(f"Generating comprehensive VoIP PCAP: {filename}")
    print(f"Creating {num_calls} different VoIP call scenarios...")
    
    # Scenario 1: Normal SIP call with RTP
    print("1. Creating normal SIP call with RTP stream...")
    call_id = f"normal-call-{call_counter}@voip.example.com"
    caller_ip = "192.168.1.100"
    callee_ip = "192.168.1.200"
    
    # SIP INVITE
    sip_invite = f"""INVITE sip:bob@{callee_ip} SIP/2.0
Via: SIP/2.0/UDP {caller_ip}:5060;branch=z9hG4bK776asdhds
Max-Forwards: 70
To: Bob <sip:bob@{callee_ip}>
From: Alice <sip:alice@{caller_ip}>;tag=1928301774
Call-ID: {call_id}
CSeq: 314159 INVITE
Contact: <sip:alice@{caller_ip}>
Content-Type: application/sdp
Content-Length: 142

v=0
o=alice 2890844526 2890844526 IN IP4 {caller_ip}
s=-
c=IN IP4 {caller_ip}
t=0 0
m=audio 8000 RTP/AVP 0
a=rtpmap:0 PCMU/8000"""
    
    pkt = Ether()/IP(src=caller_ip, dst=callee_ip)/UDP(sport=5060, dport=5060)/Raw(load=sip_invite)
    pkt.time = current_time
    packets.append(pkt)
    current_time += 0.1
    
    # SIP 200 OK
    sip_ok = f"""SIP/2.0 200 OK
Via: SIP/2.0/UDP {caller_ip}:5060;branch=z9hG4bK776asdhds
To: Bob <sip:bob@{callee_ip}>;tag=a6c85cf
From: Alice <sip:alice@{caller_ip}>;tag=1928301774
Call-ID: {call_id}
CSeq: 314159 INVITE
Contact: <sip:bob@{callee_ip}>
Content-Type: application/sdp
Content-Length: 131

v=0
o=bob 2890844527 2890844527 IN IP4 {callee_ip}
s=-
c=IN IP4 {callee_ip}
t=0 0
m=audio 8001 RTP/AVP 0
a=rtpmap:0 PCMU/8000"""
    
    pkt = Ether()/IP(src=callee_ip, dst=caller_ip)/UDP(sport=5060, dport=5060)/Raw(load=sip_ok)
    pkt.time = current_time
    packets.append(pkt)
    current_time += 0.1
    
    # RTP stream (bidirectional)
    for i in range(50):
        # Caller to callee RTP
        timestamp = int((current_time - int(current_time)) * 8000) % (2**32)  # Ensure 32-bit range
        rtp_payload = b'\x80\x00' + struct.pack('>H', i % 65536) + struct.pack('>I', timestamp) + struct.pack('>I', 0x12345678) + b'\x00' * 160
        pkt = Ether()/IP(src=caller_ip, dst=callee_ip)/UDP(sport=8000, dport=8001)/Raw(load=rtp_payload)
        pkt.time = current_time
        packets.append(pkt)
        
        # Callee to caller RTP
        rtp_payload = b'\x80\x00' + struct.pack('>H', i % 65536) + struct.pack('>I', timestamp) + struct.pack('>I', 0x87654321) + b'\x00' * 160
        pkt = Ether()/IP(src=callee_ip, dst=caller_ip)/UDP(sport=8001, dport=8000)/Raw(load=rtp_payload)
        pkt.time = current_time + 0.01
        packets.append(pkt)
        
        current_time += 0.02  # 50 packets per second
    
    # SIP BYE
    sip_bye = f"""BYE sip:bob@{callee_ip} SIP/2.0
Via: SIP/2.0/UDP {caller_ip}:5060;branch=z9hG4bK776bye
Max-Forwards: 70
To: Bob <sip:bob@{callee_ip}>;tag=a6c85cf
From: Alice <sip:alice@{caller_ip}>;tag=1928301774
Call-ID: {call_id}
CSeq: 314160 BYE
Content-Length: 0"""
    
    pkt = Ether()/IP(src=caller_ip, dst=callee_ip)/UDP(sport=5060, dport=5060)/Raw(load=sip_bye)
    pkt.time = current_time
    packets.append(pkt)
    current_time += 2.0
    call_counter += 1
    
    # Scenario 2: Suspicious call (anomaly)
    print("2. Creating suspicious call with anomalous patterns...")
    call_id = f"suspicious-call-{call_counter}@malicious.com"
    attacker_ip = "203.0.113.100"  # Suspicious external IP
    victim_ip = "192.168.1.50"
    
    # Suspicious SIP INVITE with large packet
    sip_invite = f"""INVITE sip:victim@{victim_ip} SIP/2.0
Via: SIP/2.0/UDP {attacker_ip}:5060;branch=z9hG4bKsuspicious
Max-Forwards: 70
To: Victim <sip:victim@{victim_ip}>
From: Attacker <sip:attacker@{attacker_ip}>;tag=suspicious123
Call-ID: {call_id}
CSeq: 666 INVITE
Contact: <sip:attacker@{attacker_ip}>
Content-Type: application/sdp
Content-Length: 500
User-Agent: ScanTool/1.0
X-Suspicious: yes

v=0
o=attacker 1234567890 1234567890 IN IP4 {attacker_ip}
s=Suspicious Session
c=IN IP4 {attacker_ip}
t=0 0
m=audio 9999 RTP/AVP 0
a=rtpmap:0 PCMU/8000
a=tool:scanner
""" + "a=padding:" + "X" * 300  # Large packet with padding
    
    pkt = Ether()/IP(src=attacker_ip, dst=victim_ip)/UDP(sport=5060, dport=5060)/Raw(load=sip_invite)
    pkt.time = current_time
    packets.append(pkt)
    current_time += 0.5
    
    # No RTP follow-up (suspicious pattern)
    call_counter += 1
    
    # Scenario 3: H.323 call
    print("3. Creating H.323 call scenario...")
    h323_caller = "10.0.1.100"
    h323_callee = "10.0.1.200"
    
    # H.323 RAS Registration
    h323_rrq = b'\x08\x80\x01\x00' + b'\x00' * 20  # Simplified H.323 RRQ
    pkt = Ether()/IP(src=h323_caller, dst="10.0.1.1")/UDP(sport=1719, dport=1719)/Raw(load=h323_rrq)
    pkt.time = current_time
    packets.append(pkt)
    current_time += 0.1
    
    # H.323 Call setup
    h323_setup = b'\x08\x01\x00\x00' + b'\x00' * 30  # Simplified H.323 Setup
    pkt = Ether()/IP(src=h323_caller, dst=h323_callee)/TCP(sport=1720, dport=1720)/Raw(load=h323_setup)
    pkt.time = current_time
    packets.append(pkt)
    current_time += 2.0
    
    # Scenario 4: Multiple rapid calls (burst pattern)
    print("4. Creating burst pattern with multiple rapid calls...")
    for burst_call in range(3):
        call_id = f"burst-call-{burst_call}@burst.example.com"
        burst_caller = "172.16.1.10"
        burst_callee = f"172.16.1.{20 + burst_call}"
        
        sip_invite = f"""INVITE sip:user{burst_call}@{burst_callee} SIP/2.0
Via: SIP/2.0/UDP {burst_caller}:5060;branch=z9hG4bKburst{burst_call}
To: User{burst_call} <sip:user{burst_call}@{burst_callee}>
From: Caller <sip:caller@{burst_caller}>;tag=burst{burst_call}
Call-ID: {call_id}
CSeq: {1000 + burst_call} INVITE
Content-Length: 0"""
        
        pkt = Ether()/IP(src=burst_caller, dst=burst_callee)/UDP(sport=5060, dport=5060)/Raw(load=sip_invite)
        pkt.time = current_time
        packets.append(pkt)
        current_time += 0.1  # Very rapid calls
    
    current_time += 1.0
    
    # Scenario 5: MGCP call
    print("5. Creating MGCP call scenario...")
    mgcp_gateway = "192.168.10.100"
    mgcp_controller = "192.168.10.1"
    
    # MGCP CRCX (Create Connection)
    mgcp_crcx = f"""CRCX 2000 aaln/1@{mgcp_gateway} MGCP 1.0
C: A3C47F21456789F0
L: p:20, a:PCMU
M: sendrecv
X: 0123456789ABCDEF"""
    
    pkt = Ether()/IP(src=mgcp_controller, dst=mgcp_gateway)/UDP(sport=2427, dport=2427)/Raw(load=mgcp_crcx)
    pkt.time = current_time
    packets.append(pkt)
    current_time += 0.1
    
    # MGCP response
    mgcp_response = """200 2000 OK
I: FDE234C8
v=0
o=- 25678 753849 IN IP4 192.168.10.100
c=IN IP4 192.168.10.100
t=0 0
m=audio 3456 RTP/AVP 0"""
    
    pkt = Ether()/IP(src=mgcp_gateway, dst=mgcp_controller)/UDP(sport=2427, dport=2427)/Raw(load=mgcp_response)
    pkt.time = current_time
    packets.append(pkt)
    current_time += 1.0
    
    # Scenario 6: RTCP packets
    print("6. Adding RTCP control packets...")
    rtcp_sender = "192.168.1.100"
    rtcp_receiver = "192.168.1.200"
    
    # RTCP Sender Report
    rtcp_sr = b'\x80\xc8\x00\x06' + struct.pack('>I', 0x12345678) + b'\x00' * 20
    pkt = Ether()/IP(src=rtcp_sender, dst=rtcp_receiver)/UDP(sport=8001, dport=8001)/Raw(load=rtcp_sr)
    pkt.time = current_time
    packets.append(pkt)
    current_time += 0.1
    
    # RTCP Receiver Report
    rtcp_rr = b'\x81\xc9\x00\x07' + struct.pack('>I', 0x87654321) + b'\x00' * 24
    pkt = Ether()/IP(src=rtcp_receiver, dst=rtcp_sender)/UDP(sport=8001, dport=8001)/Raw(load=rtcp_rr)
    pkt.time = current_time
    packets.append(pkt)
    
    # Write the PCAP file
    print(f"Writing {len(packets)} packets to {filename}...")
    wrpcap(filename, packets)
    
    print(f"✅ Generated comprehensive VoIP PCAP file: {filename}")
    print(f"📊 Statistics:")
    print(f"   - Total packets: {len(packets)}")
    print(f"   - Scenarios included:")
    print(f"     * Normal SIP call with RTP stream")
    print(f"     * Suspicious/anomalous call pattern")
    print(f"     * H.323 protocol traffic")
    print(f"     * Burst calling pattern")
    print(f"     * MGCP gateway protocol")
    print(f"     * RTCP control packets")
    print(f"   - File size: ~{os.path.getsize(filename) / 1024:.1f} KB")
    
    return filename

if __name__ == "__main__":
    import os
    import struct
    
    # Generate the comprehensive PCAP file
    filename = generate_comprehensive_voip_pcap()
    
    print(f"\n🎉 PCAP file ready for download: {filename}")
    print(f"📁 Full path: {os.path.abspath(filename)}")
    print(f"\nYou can now:")
    print(f"1. Download this file from: {os.path.abspath(filename)}")
    print(f"2. Use it to test VoIP analysis tools")
    print(f"3. Upload it to the VoIP Tracer web interface")
    print(f"4. Share it for testing purposes")
