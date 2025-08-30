#!/usr/bin/env python3
"""
Generate large and diverse PCAP files for VoIP analysis testing.
Creates realistic VoIP traffic patterns with various protocols and scenarios.
"""

from scapy.all import Ether, IP, UDP, TCP, Raw, wrpcap
import random
import time
import ipaddress
import struct
import os
from datetime import datetime, timedelta

def generate_diverse_voip_pcap(filename="large_diverse_voip_traffic.pcap", num_calls=500, duration_hours=24):
    """
    Generate a large, diverse PCAP file with realistic VoIP traffic patterns.
    
    Args:
        filename: Output PCAP filename
        num_calls: Number of VoIP calls to simulate
        duration_hours: Time span for the traffic (in hours)
    """
    
    packets = []
    base_time = time.time() - (duration_hours * 3600)  # Start X hours ago
    
    # Define realistic network segments
    office_networks = [
        "192.168.1.0/24",    # Main office
        "192.168.2.0/24",    # Branch office
        "10.0.1.0/24",       # VoIP VLAN
        "10.0.2.0/24",       # Executive VLAN
    ]
    
    external_ips = [
        "203.0.113.10",      # External SIP provider
        "198.51.100.20",     # Backup provider
        "8.8.8.8",           # Public DNS (for contrast)
        "151.101.1.140",     # External service
        "185.199.108.153",   # CDN
    ]
    
    # VoIP server IPs
    voip_servers = [
        "10.0.1.10",         # Primary PBX
        "10.0.1.11",         # Secondary PBX
        "192.168.1.5",       # SIP proxy
    ]
    
    print(f"🎯 Generating {num_calls} VoIP calls over {duration_hours} hours...")
    
    for call_idx in range(num_calls):
        # Generate call timing
        call_start = base_time + random.uniform(0, duration_hours * 3600)
        call_duration = random.choice([
            random.uniform(5, 30),      # Short calls (30%)
            random.uniform(30, 180),    # Normal calls (40%)
            random.uniform(180, 1800),  # Long calls (25%)
            random.uniform(1800, 7200), # Very long calls (5%)
        ])
        
        # Call type determines pattern
        call_type = random.choices(
            ['normal', 'suspicious', 'international', 'internal', 'conference'],
            weights=[40, 10, 15, 25, 10]
        )[0]
        
        # Generate call participants based on type
        if call_type == 'internal':
            src_network = random.choice(office_networks[:2])
            dst_network = random.choice(office_networks[:2])
            src_ip = str(random.choice(list(ipaddress.IPv4Network(src_network).hosts())))
            dst_ip = str(random.choice(list(ipaddress.IPv4Network(dst_network).hosts())))
        elif call_type == 'suspicious':
            src_ip = str(random.choice(list(ipaddress.IPv4Network(office_networks[0]).hosts())))
            dst_ip = random.choice(external_ips)
        elif call_type == 'international':
            src_ip = str(random.choice(list(ipaddress.IPv4Network(office_networks[0]).hosts())))
            dst_ip = random.choice(external_ips)
            call_duration *= 0.7  # International calls often shorter
        elif call_type == 'conference':
            src_ip = random.choice(voip_servers)
            dst_ip = str(random.choice(list(ipaddress.IPv4Network(office_networks[2]).hosts())))
            call_duration *= 2.5  # Conference calls longer
        else:  # normal
            src_ip = str(random.choice(list(ipaddress.IPv4Network(office_networks[0]).hosts())))
            dst_ip = random.choice(voip_servers)
        
        # Generate unique call ID
        call_id = f"call-{call_type}-{call_idx:04d}-{int(call_start)}"
        
        # Generate SIP signaling packets
        packets.extend(generate_sip_flow(
            src_ip, dst_ip, call_id, call_start, call_duration, call_type
        ))
        
        # Generate RTP media packets
        if call_duration > 2:  # Only generate media for established calls
            packets.extend(generate_rtp_flow(
                src_ip, dst_ip, call_start + 2, call_duration - 4, call_type
            ))
        
        if call_idx % 50 == 0:
            print(f"   Generated call {call_idx}/{num_calls} ({call_type})")
    
    # Add some background network traffic for realism
    print("🌐 Adding background network traffic...")
    packets.extend(generate_background_traffic(base_time, duration_hours, office_networks))
    
    # Add suspicious scanning activity
    print("🚨 Adding suspicious scanning patterns...")
    packets.extend(generate_suspicious_activity(base_time, duration_hours, office_networks))
    
    # Sort packets by timestamp
    print("⏰ Sorting packets by timestamp...")
    packets.sort(key=lambda p: p.time)
    
    # Write to PCAP file
    print(f"💾 Writing {len(packets)} packets to {filename}...")
    wrpcap(filename, packets)
    
    # Generate statistics
    file_size = os.path.getsize(filename) / (1024*1024)  # MB
    print(f"✅ Generated {filename}")
    print(f"   📊 {len(packets)} packets")
    print(f"   📏 {file_size:.2f} MB")
    print(f"   🕐 {duration_hours} hours of traffic")
    print(f"   📞 {num_calls} VoIP calls")

def generate_sip_flow(src_ip, dst_ip, call_id, start_time, duration, call_type):
    """Generate SIP signaling packets for a call."""
    packets = []
    
    # SIP messages timing
    invite_time = start_time
    trying_time = invite_time + random.uniform(0.1, 0.5)
    ringing_time = trying_time + random.uniform(0.5, 2.0)
    ok_time = ringing_time + random.uniform(1.0, 5.0)
    ack_time = ok_time + random.uniform(0.1, 0.3)
    bye_time = start_time + duration
    bye_ok_time = bye_time + random.uniform(0.1, 0.5)
    
    # Determine if call is successful
    call_success = random.random() > (0.3 if call_type == 'suspicious' else 0.05)
    
    # INVITE
    invite_pkt = generate_sip_packet(
        src_ip, dst_ip, 5060, 5060, invite_time,
        f"INVITE sip:user@{dst_ip} SIP/2.0\r\nCall-ID: {call_id}\r\nFrom: <sip:caller@{src_ip}>\r\nTo: <sip:user@{dst_ip}>\r\n"
    )
    packets.append(invite_pkt)
    
    # 100 Trying
    trying_pkt = generate_sip_packet(
        dst_ip, src_ip, 5060, 5060, trying_time,
        f"SIP/2.0 100 Trying\r\nCall-ID: {call_id}\r\n"
    )
    packets.append(trying_pkt)
    
    if call_success:
        # 180 Ringing
        ringing_pkt = generate_sip_packet(
            dst_ip, src_ip, 5060, 5060, ringing_time,
            f"SIP/2.0 180 Ringing\r\nCall-ID: {call_id}\r\n"
        )
        packets.append(ringing_pkt)
        
        # 200 OK
        ok_pkt = generate_sip_packet(
            dst_ip, src_ip, 5060, 5060, ok_time,
            f"SIP/2.0 200 OK\r\nCall-ID: {call_id}\r\n"
        )
        packets.append(ok_pkt)
        
        # ACK
        ack_pkt = generate_sip_packet(
            src_ip, dst_ip, 5060, 5060, ack_time,
            f"ACK sip:user@{dst_ip} SIP/2.0\r\nCall-ID: {call_id}\r\n"
        )
        packets.append(ack_pkt)
        
        # BYE
        bye_pkt = generate_sip_packet(
            src_ip, dst_ip, 5060, 5060, bye_time,
            f"BYE sip:user@{dst_ip} SIP/2.0\r\nCall-ID: {call_id}\r\n"
        )
        packets.append(bye_pkt)
        
        # 200 OK for BYE
        bye_ok_pkt = generate_sip_packet(
            dst_ip, src_ip, 5060, 5060, bye_ok_time,
            f"SIP/2.0 200 OK\r\nCall-ID: {call_id}\r\n"
        )
        packets.append(bye_ok_pkt)
    else:
        # Call rejected
        reject_time = ringing_time + random.uniform(0.5, 2.0)
        reject_codes = ["486 Busy Here", "603 Decline", "404 Not Found", "408 Request Timeout"]
        reject_pkt = generate_sip_packet(
            dst_ip, src_ip, 5060, 5060, reject_time,
            f"SIP/2.0 {random.choice(reject_codes)}\r\nCall-ID: {call_id}\r\n"
        )
        packets.append(reject_pkt)
    
    return packets

def generate_sip_packet(src_ip, dst_ip, src_port, dst_port, timestamp, sip_content):
    """Generate a single SIP packet."""
    pkt = Ether() / IP(src=src_ip, dst=dst_ip) / UDP(sport=src_port, dport=dst_port) / Raw(load=sip_content)
    pkt.time = timestamp
    return pkt

def generate_rtp_flow(src_ip, dst_ip, start_time, duration, call_type):
    """Generate RTP media packets for a call."""
    packets = []
    
    # RTP parameters
    src_rtp_port = random.randint(16384, 32767)
    dst_rtp_port = random.randint(16384, 32767)
    ssrc = random.randint(1000000, 9999999999)
    
    # Packet characteristics based on call type
    if call_type == 'conference':
        packet_interval = 0.020  # 20ms for conference (G.711)
        payload_size = 160
    elif call_type == 'suspicious':
        packet_interval = random.uniform(0.015, 0.025)  # Irregular timing
        payload_size = random.randint(80, 200)
    else:
        packet_interval = 0.020  # Standard 20ms
        payload_size = 160  # G.711 payload
    
    current_time = start_time
    seq_num = random.randint(1000, 65000)
    
    while current_time < start_time + duration:
        # Generate bidirectional RTP
        
        # Forward direction
        rtp_pkt1 = generate_rtp_packet(
            src_ip, dst_ip, src_rtp_port, dst_rtp_port,
            current_time, ssrc, seq_num, payload_size
        )
        packets.append(rtp_pkt1)
        
        # Reverse direction (with slight delay)
        rtp_pkt2 = generate_rtp_packet(
            dst_ip, src_ip, dst_rtp_port, src_rtp_port,
            current_time + 0.001, ssrc + 1, seq_num + 1, payload_size
        )
        packets.append(rtp_pkt2)
        
        current_time += packet_interval
        seq_num += 2
        
        # Add some packet loss/jitter for realism
        if random.random() < 0.001:  # 0.1% packet loss
            current_time += packet_interval  # Skip a packet
        if random.random() < 0.05:  # 5% jitter
            current_time += random.uniform(-0.005, 0.005)
    
    return packets

def generate_rtp_packet(src_ip, dst_ip, src_port, dst_port, timestamp, ssrc, seq_num, payload_size):
    """Generate a single RTP packet."""
    # Basic RTP header (12 bytes) + payload
    rtp_timestamp = int(timestamp * 8000) & 0xFFFFFFFF  # Timestamp for 8kHz
    
    rtp_header = struct.pack('!BBHII', 
                           0x80,  # Version=2, Padding=0, Extension=0, CC=0
                           0x00,  # Marker=0, Payload Type=0 (PCMU)
                           seq_num & 0xFFFF,
                           rtp_timestamp,
                           ssrc & 0xFFFFFFFF)
    
    payload = b'\x00' * payload_size  # Dummy audio payload
    
    pkt = Ether() / IP(src=src_ip, dst=dst_ip) / UDP(sport=src_port, dport=dst_port) / Raw(load=rtp_header + payload)
    pkt.time = timestamp
    return pkt

def generate_background_traffic(base_time, duration_hours, networks):
    """Generate background network traffic for realism."""
    packets = []
    
    # Generate some HTTP, HTTPS, DNS traffic
    protocols = [
        ('HTTP', 80, 1024),
        ('HTTPS', 443, 1024),
        ('DNS', 53, 64),
        ('NTP', 123, 48),
        ('DHCP', 67, 300),
    ]
    
    for _ in range(200):  # 200 background flows
        start_time = base_time + random.uniform(0, duration_hours * 3600)
        src_ip = str(random.choice(list(ipaddress.IPv4Network(random.choice(networks)).hosts())))
        
        proto_name, dst_port, size = random.choice(protocols)
        
        if proto_name == 'DNS':
            dst_ip = "8.8.8.8"
        elif proto_name in ['HTTP', 'HTTPS']:
            dst_ip = "151.101.1.140"  # External web server
        else:
            dst_ip = str(random.choice(list(ipaddress.IPv4Network(networks[0]).hosts())))
        
        # Generate a few packets for this flow
        for i in range(random.randint(1, 10)):
            pkt_time = start_time + i * random.uniform(0.1, 2.0)
            src_port = random.randint(32768, 65535)
            
            pkt = Ether() / IP(src=src_ip, dst=dst_ip) / UDP(sport=src_port, dport=dst_port) / Raw(load=b'X' * size)
            pkt.time = pkt_time
            packets.append(pkt)
    
    return packets

def generate_suspicious_activity(base_time, duration_hours, networks):
    """Generate suspicious scanning and attack patterns."""
    packets = []
    
    # Port scanning activity
    scanner_ip = str(random.choice(list(ipaddress.IPv4Network(networks[0]).hosts())))
    scan_start = base_time + random.uniform(0, duration_hours * 3600 * 0.5)
    
    # Scan common VoIP ports
    voip_ports = [5060, 5061, 1719, 1720, 2000, 4569, 5036, 5038]
    target_network = ipaddress.IPv4Network(networks[2])  # VoIP VLAN
    
    for target_ip in list(target_network.hosts())[:50]:  # Scan first 50 IPs
        for port in voip_ports:
            scan_time = scan_start + random.uniform(0, 600)  # Over 10 minutes
            
            # SYN scan packet
            pkt = Ether() / IP(src=scanner_ip, dst=str(target_ip)) / TCP(sport=random.randint(32768, 65535), dport=port, flags='S')
            pkt.time = scan_time
            packets.append(pkt)
    
    # Rapid SIP INVITE flood (potential DoS)
    flood_start = base_time + random.uniform(duration_hours * 3600 * 0.7, duration_hours * 3600 * 0.9)
    attacker_ip = "203.0.113.666"  # Obvious external attacker
    target_server = "10.0.1.10"   # VoIP server
    
    for i in range(100):  # 100 rapid INVITEs
        flood_time = flood_start + i * 0.1  # Every 100ms
        
        invite_content = f"INVITE sip:victim{i}@{target_server} SIP/2.0\r\nCall-ID: flood-{i}\r\nFrom: <sip:attacker@{attacker_ip}>\r\n"
        
        pkt = Ether() / IP(src=attacker_ip, dst=target_server) / UDP(sport=5060, dport=5060) / Raw(load=invite_content)
        pkt.time = flood_time
        packets.append(pkt)
    
    return packets

if __name__ == "__main__":
    print("🎯 VoIP PCAP Generator")
    print("=" * 50)
    
    # Generate different sizes of PCAP files
    configs = [
        ("small_diverse_voip.pcap", 100, 2),      # Small: 100 calls, 2 hours
        ("medium_diverse_voip.pcap", 300, 8),     # Medium: 300 calls, 8 hours  
        ("large_diverse_voip.pcap", 1000, 24),    # Large: 1000 calls, 24 hours
        ("huge_diverse_voip.pcap", 2500, 72),     # Huge: 2500 calls, 72 hours
    ]
    
    for filename, num_calls, duration in configs:
        print(f"\n🎬 Generating {filename}...")
        generate_diverse_voip_pcap(filename, num_calls, duration)
    
    print("\n🎉 All PCAP files generated successfully!")
    print("\nFiles created:")
    for filename, _, _ in configs:
        if os.path.exists(filename):
            size_mb = os.path.getsize(filename) / (1024*1024)
            print(f"  📁 {filename}: {size_mb:.2f} MB")
