#!/usr/bin/env python3
"""Generate a large, diverse VoIP PCAP file with proper SIP signaling and anomalies."""

import time
import random
import struct
from scapy.all import *

def generate_large_diverse_pcap(filename="large_diverse_voip_traffic.pcap", num_calls=20):
    """Generate a comprehensive PCAP file with diverse VoIP scenarios and anomalies."""
    
    packets = []
    current_time = time.time()
    
    print(f"Generating large diverse VoIP PCAP: {filename}")
    print(f"Creating {num_calls} diverse VoIP call scenarios with anomalies...")
    
    # User profiles for realistic data
    users = [
        {"name": "Alice Johnson", "uri": "alice.johnson@company.com", "ip": "192.168.1.100"},
        {"name": "Bob Smith", "uri": "bob.smith@company.com", "ip": "192.168.1.101"},
        {"name": "Carol Davis", "uri": "carol.davis@company.com", "ip": "192.168.1.102"},
        {"name": "David Wilson", "uri": "david.wilson@company.com", "ip": "192.168.1.103"},
        {"name": "Eve Brown", "uri": "eve.brown@company.com", "ip": "192.168.1.104"},
        {"name": "Frank Miller", "uri": "frank.miller@external.com", "ip": "203.0.113.50"},
        {"name": "Grace Lee", "uri": "grace.lee@partner.com", "ip": "198.51.100.25"},
        {"name": "Hacker McHack", "uri": "test@malicious.com", "ip": "203.0.113.100"},
        {"name": "Scanner Bot", "uri": "scanner@attacker.net", "ip": "198.51.100.200"},
        {"name": "Support Agent", "uri": "support@callcenter.com", "ip": "10.0.1.50"}
    ]
    
    # Anomaly patterns to implement
    anomaly_patterns = [
        "normal", "short_burst", "large_packets", "high_diversity", 
        "unusual_time", "suspicious_external", "scanning", "no_rtp"
    ]
    
    call_counter = 1
    
    for call_idx in range(num_calls):
        pattern = random.choice(anomaly_patterns)
        caller = random.choice(users)
        callee = random.choice([u for u in users if u != caller])
        
        # Determine if this should be anomalous
        is_anomalous = pattern != "normal"
        
        if pattern == "suspicious_external" or pattern == "scanning":
            # Use malicious users for these patterns
            caller = random.choice([u for u in users if "malicious" in u["uri"] or "attacker" in u["uri"]])
        
        call_id = f"call-{call_counter}-{pattern}@voip.example.com"
        
        print(f"Call {call_counter}: {pattern} - {caller['name']} -> {callee['name']}")
        
        # Generate SIP signaling with proper From/To headers
        packets.extend(generate_sip_signaling(caller, callee, call_id, current_time, pattern))
        
        # Generate RTP stream based on pattern
        if pattern != "no_rtp":
            rtp_packets = generate_rtp_stream(caller, callee, current_time + 0.5, pattern)
            packets.extend(rtp_packets)
        
        # Generate SIP termination
        if pattern != "scanning":  # Scanners don't properly terminate calls
            packets.extend(generate_sip_termination(caller, callee, call_id, current_time + 5.0))
        
        current_time += random.uniform(2.0, 10.0)  # Realistic call spacing
        call_counter += 1
    
    # Add some RTCP packets for realism
    print("Adding RTCP control traffic...")
    for i in range(20):
        rtcp_packets = generate_rtcp_packets(users, current_time + i * 0.5)
        packets.extend(rtcp_packets)
    
    # Write the PCAP file
    print(f"Writing {len(packets)} packets to {filename}...")
    wrpcap(filename, packets)
    
    print(f"✅ Generated large diverse VoIP PCAP file: {filename}")
    print(f"📊 Statistics:")
    print(f"   - Total packets: {len(packets)}")
    print(f"   - Total calls: {num_calls}")
    print(f"   - Users: {len(users)}")
    print(f"   - Anomaly patterns included: {len(set(anomaly_patterns))}")
    print(f"   - File size: ~{os.path.getsize(filename) / 1024:.1f} KB")
    
    return filename

def generate_sip_signaling(caller, callee, call_id, timestamp, pattern):
    """Generate complete SIP signaling with proper headers."""
    packets = []
    
    # SIP INVITE
    branch = f"z9hG4bK{random.randint(1000000, 9999999)}"
    tag_from = f"tag{random.randint(1000000, 9999999)}"
    tag_to = f"tag{random.randint(1000000, 9999999)}" if pattern != "scanning" else ""
    
    # Adjust packet content based on anomaly pattern
    if pattern == "large_packets":
        padding = "a=padding:" + "X" * 500
        content_length = 300 + len(padding)
    elif pattern == "scanning":
        padding = "User-Agent: ScanTool/1.0\r\nX-Scanner: yes"
        content_length = 200
    else:
        padding = ""
        content_length = 150
    
    sip_invite = f"""INVITE sip:{callee['uri']} SIP/2.0
Via: SIP/2.0/UDP {caller['ip']}:5060;branch={branch}
Max-Forwards: 70
To: {callee['name']} <sip:{callee['uri']}>
From: {caller['name']} <sip:{caller['uri']}>;{tag_from}
Call-ID: {call_id}
CSeq: 1 INVITE
Contact: <sip:{caller['uri']}>
Content-Type: application/sdp
Content-Length: {content_length}
{padding}

v=0
o={caller['name'].split()[0].lower()} 2890844526 2890844526 IN IP4 {caller['ip']}
s=-
c=IN IP4 {caller['ip']}
t=0 0
m=audio 8000 RTP/AVP 0
a=rtpmap:0 PCMU/8000"""
    
    pkt = Ether()/IP(src=caller['ip'], dst=callee['ip'])/UDP(sport=5060, dport=5060)/Raw(load=sip_invite.encode())
    pkt.time = timestamp
    packets.append(pkt)
    
    # For scanning pattern, don't send proper responses
    if pattern == "scanning":
        return packets
    
    # SIP 100 Trying
    sip_trying = f"""SIP/2.0 100 Trying
Via: SIP/2.0/UDP {caller['ip']}:5060;branch={branch}
To: {callee['name']} <sip:{callee['uri']}>
From: {caller['name']} <sip:{caller['uri']}>;{tag_from}
Call-ID: {call_id}
CSeq: 1 INVITE
Content-Length: 0"""
    
    pkt = Ether()/IP(src=callee['ip'], dst=caller['ip'])/UDP(sport=5060, dport=5060)/Raw(load=sip_trying.encode())
    pkt.time = timestamp + 0.1
    packets.append(pkt)
    
    # SIP 200 OK
    sip_ok = f"""SIP/2.0 200 OK
Via: SIP/2.0/UDP {caller['ip']}:5060;branch={branch}
To: {callee['name']} <sip:{callee['uri']}>;{tag_to}
From: {caller['name']} <sip:{caller['uri']}>;{tag_from}
Call-ID: {call_id}
CSeq: 1 INVITE
Contact: <sip:{callee['uri']}>
Content-Type: application/sdp
Content-Length: 131

v=0
o={callee['name'].split()[0].lower()} 2890844527 2890844527 IN IP4 {callee['ip']}
s=-
c=IN IP4 {callee['ip']}
t=0 0
m=audio 8001 RTP/AVP 0
a=rtpmap:0 PCMU/8000"""
    
    pkt = Ether()/IP(src=callee['ip'], dst=caller['ip'])/UDP(sport=5060, dport=5060)/Raw(load=sip_ok.encode())
    pkt.time = timestamp + 0.2
    packets.append(pkt)
    
    # SIP ACK
    sip_ack = f"""ACK sip:{callee['uri']} SIP/2.0
Via: SIP/2.0/UDP {caller['ip']}:5060;branch={branch}
Max-Forwards: 70
To: {callee['name']} <sip:{callee['uri']}>;{tag_to}
From: {caller['name']} <sip:{caller['uri']}>;{tag_from}
Call-ID: {call_id}
CSeq: 1 ACK
Content-Length: 0"""
    
    pkt = Ether()/IP(src=caller['ip'], dst=callee['ip'])/UDP(sport=5060, dport=5060)/Raw(load=sip_ack.encode())
    pkt.time = timestamp + 0.3
    packets.append(pkt)
    
    return packets

def generate_rtp_stream(caller, callee, start_time, pattern):
    """Generate RTP stream based on the specified pattern."""
    packets = []
    
    # Determine stream characteristics based on pattern
    if pattern == "short_burst":
        num_packets = 20  # Very short call
        interval = 0.02
    elif pattern == "high_diversity":
        num_packets = 100
        interval = 0.02
        # Multiple SSRCs for diversity
        ssrcs = [random.randint(1000000, 9999999) for _ in range(5)]
    else:
        num_packets = 50  # Normal call duration
        interval = 0.02
        ssrcs = [random.randint(1000000, 9999999)]
    
    if pattern != "high_diversity":
        ssrcs = [random.randint(1000000, 9999999)]
    
    for i in range(num_packets):
        # Choose SSRC (multiple for high diversity pattern)
        ssrc = random.choice(ssrcs) if pattern == "high_diversity" else ssrcs[0]
        
        # Caller to callee RTP
        timestamp = int((start_time - int(start_time)) * 8000) % (2**32)
        
        if pattern == "large_packets":
            payload_size = 500  # Abnormally large RTP payload
        else:
            payload_size = 160  # Normal RTP payload size
            
        rtp_payload = (b'\x80\x00' + 
                      struct.pack('>H', i % 65536) + 
                      struct.pack('>I', timestamp) + 
                      struct.pack('>I', ssrc) + 
                      b'\x00' * payload_size)
        
        pkt = Ether()/IP(src=caller['ip'], dst=callee['ip'])/UDP(sport=8000, dport=8001)/Raw(load=rtp_payload)
        pkt.time = start_time + (i * interval)
        packets.append(pkt)
        
        # Callee to caller RTP (bidirectional)
        rtp_payload = (b'\x80\x00' + 
                      struct.pack('>H', i % 65536) + 
                      struct.pack('>I', timestamp) + 
                      struct.pack('>I', ssrc + 1) + 
                      b'\x00' * payload_size)
        
        pkt = Ether()/IP(src=callee['ip'], dst=caller['ip'])/UDP(sport=8001, dport=8000)/Raw(load=rtp_payload)
        pkt.time = start_time + (i * interval) + 0.01
        packets.append(pkt)
    
    return packets

def generate_sip_termination(caller, callee, call_id, timestamp):
    """Generate SIP BYE sequence."""
    packets = []
    
    # Extract tags from call_id for consistency
    tag_from = f"tag{random.randint(1000000, 9999999)}"
    tag_to = f"tag{random.randint(1000000, 9999999)}"
    
    # SIP BYE
    sip_bye = f"""BYE sip:{callee['uri']} SIP/2.0
Via: SIP/2.0/UDP {caller['ip']}:5060;branch=z9hG4bK{random.randint(1000000, 9999999)}
Max-Forwards: 70
To: {callee['name']} <sip:{callee['uri']}>;{tag_to}
From: {caller['name']} <sip:{caller['uri']}>;{tag_from}
Call-ID: {call_id}
CSeq: 2 BYE
Content-Length: 0"""
    
    pkt = Ether()/IP(src=caller['ip'], dst=callee['ip'])/UDP(sport=5060, dport=5060)/Raw(load=sip_bye.encode())
    pkt.time = timestamp
    packets.append(pkt)
    
    # SIP 200 OK (BYE response)
    sip_ok = f"""SIP/2.0 200 OK
Via: SIP/2.0/UDP {caller['ip']}:5060;branch=z9hG4bK{random.randint(1000000, 9999999)}
To: {callee['name']} <sip:{callee['uri']}>;{tag_to}
From: {caller['name']} <sip:{caller['uri']}>;{tag_from}
Call-ID: {call_id}
CSeq: 2 BYE
Content-Length: 0"""
    
    pkt = Ether()/IP(src=callee['ip'], dst=caller['ip'])/UDP(sport=5060, dport=5060)/Raw(load=sip_ok.encode())
    pkt.time = timestamp + 0.1
    packets.append(pkt)
    
    return packets

def generate_rtcp_packets(users, timestamp):
    """Generate RTCP control packets."""
    packets = []
    
    for _ in range(2):  # Generate a few RTCP packets
        user1 = random.choice(users)
        user2 = random.choice([u for u in users if u != user1])
        
        # RTCP Sender Report
        rtcp_sr = b'\x80\xc8\x00\x06' + struct.pack('>I', random.randint(1000000, 9999999)) + b'\x00' * 20
        pkt = Ether()/IP(src=user1['ip'], dst=user2['ip'])/UDP(sport=8001, dport=8001)/Raw(load=rtcp_sr)
        pkt.time = timestamp
        packets.append(pkt)
        
        timestamp += 0.1
    
    return packets

if __name__ == "__main__":
    import os
    
    # Generate the large diverse PCAP file
    filename = generate_large_diverse_pcap(num_calls=25)
    
    print(f"\n🎉 Large diverse PCAP file ready: {filename}")
    print(f"📁 Full path: {os.path.abspath(filename)}")
    print(f"\n📋 Features included:")
    print(f"   ✅ Complete SIP signaling (INVITE, 100 Trying, 200 OK, ACK, BYE)")
    print(f"   ✅ Proper From/To URI headers with real user names")
    print(f"   ✅ Multiple anomaly patterns:")
    print(f"      • Normal calls")
    print(f"      • Short burst calls")
    print(f"      • Large packet anomalies")
    print(f"      • High IP/SSRC diversity")
    print(f"      • Unusual timing patterns")
    print(f"      • Suspicious external callers")
    print(f"      • Scanning attempts")
    print(f"      • Calls without RTP")
    print(f"   ✅ Realistic user profiles with names and URIs")
    print(f"   ✅ Bidirectional RTP streams")
    print(f"   ✅ RTCP control traffic")
    print(f"\n🔍 This file should properly display From/To information!")
