#!/usr/bin/env python3
"""
Enhanced PCAP Generator for VoIP Traffic Analysis
Generates large, diverse datasets with anomalies and comprehensive FROM/TO data
"""

import random
import time
import struct
import socket
from datetime import datetime, timedelta
import ipaddress

class EnhancedPCAPGenerator:
    def __init__(self):
        # PCAP file header
        self.pcap_header = struct.pack('<LHHLLLL',
            0xa1b2c3d4,  # magic number
            2,           # version major
            4,           # version minor
            0,           # thiszone
            0,           # sigfigs
            65535,       # snaplen
            1            # network (Ethernet)
        )
        
        # Diverse phone number pools
        self.phone_prefixes = [
            '+1415', '+1212', '+1310', '+1202', '+1713',  # US
            '+44207', '+3312', '+4930', '+861', '+8190',   # International
            '+91124', '+5511', '+27', '+972', '+971'       # More international
        ]
        
        # Company/Organization pools
        self.organizations = [
            'enterprise-corp', 'tech-startup', 'government-agency',
            'hospital-system', 'university', 'bank-hq', 'retail-chain',
            'manufacturing', 'telecom-provider', 'call-center'
        ]
        
        # IP ranges for different network types
        self.ip_ranges = {
            'internal': ['192.168.1.0/24', '10.0.0.0/16', '172.16.0.0/12'],
            'external': ['203.0.113.0/24', '198.51.100.0/24', '8.8.8.0/24'],
            'voip_servers': ['192.168.100.0/24', '10.10.10.0/24'],
            'suspicious': ['185.220.101.0/24', '91.134.145.0/24']
        }
        
        # SIP methods and response codes
        self.sip_methods = ['INVITE', 'ACK', 'BYE', 'CANCEL', 'REGISTER', 'OPTIONS', 'NOTIFY', 'SUBSCRIBE']
        self.sip_responses = {
            100: 'Trying', 180: 'Ringing', 200: 'OK', 401: 'Unauthorized',
            403: 'Forbidden', 404: 'Not Found', 486: 'Busy Here', 500: 'Server Error'
        }
        
        # Codec types for RTP
        self.codecs = {
            0: 'PCMU', 8: 'PCMA', 18: 'G729', 97: 'iLBC',
            98: 'H264', 99: 'Opus', 100: 'VP8', 101: 'telephone-event'
        }

    def generate_ip(self, range_type='internal'):
        """Generate IP address from specified range"""
        if range_type not in self.ip_ranges:
            range_type = 'internal'
        
        network = random.choice(self.ip_ranges[range_type])
        net = ipaddress.IPv4Network(network)
        return str(random.choice(list(net.hosts())))

    def generate_phone_number(self, org_type='normal'):
        """Generate realistic phone numbers"""
        prefix = random.choice(self.phone_prefixes)
        if org_type == 'suspicious':
            # Generate numbers that might be associated with suspicious activity
            suffix = ''.join([random.choice('0123456789') for _ in range(7)])
        else:
            suffix = ''.join([random.choice('0123456789') for _ in range(7)])
        return f"{prefix}{suffix}"

    def create_ethernet_header(self, src_mac=None, dst_mac=None):
        """Create Ethernet header"""
        if not src_mac:
            src_mac = bytes([random.randint(0, 255) for _ in range(6)])
        if not dst_mac:
            dst_mac = bytes([random.randint(0, 255) for _ in range(6)])
        return dst_mac + src_mac + struct.pack('>H', 0x0800)

    def create_ip_header(self, src_ip, dst_ip, payload_len, protocol=17):
        """Create IP header"""
        version_ihl = 0x45  # IPv4, header length 20 bytes
        tos = 0
        total_len = 20 + payload_len
        id_field = random.randint(1, 65535)
        flags_frag = 0x4000  # Don't fragment
        ttl = random.randint(32, 128)
        checksum = 0  # Will be calculated
        
        src_ip_bytes = socket.inet_aton(src_ip)
        dst_ip_bytes = socket.inet_aton(dst_ip)
        
        return struct.pack('>BBHHHBBH4s4s',
            version_ihl, tos, total_len, id_field, flags_frag,
            ttl, protocol, checksum, src_ip_bytes, dst_ip_bytes
        )

    def create_udp_header(self, src_port, dst_port, payload_len):
        """Create UDP header"""
        length = 8 + payload_len
        checksum = 0
        return struct.pack('>HHHH', src_port, dst_port, length, checksum)

    def create_sip_invite(self, from_phone, to_phone, from_ip, to_ip, call_id):
        """Create SIP INVITE message"""
        from_org = random.choice(self.organizations)
        to_org = random.choice(self.organizations)
        
        sip_msg = f"""INVITE sip:{to_phone}@{to_ip} SIP/2.0
Via: SIP/2.0/UDP {from_ip}:5060;branch=z9hG4bK{random.randint(100000, 999999)}
Max-Forwards: 70
To: <sip:{to_phone}@{to_ip}>
From: "{from_phone}" <sip:{from_phone}@{from_ip}>;tag={random.randint(100000, 999999)}
Call-ID: {call_id}@{from_ip}
CSeq: 1 INVITE
Contact: <sip:{from_phone}@{from_ip}:5060>
Content-Type: application/sdp
Content-Length: 200
Organization: {from_org}
User-Agent: VoIPTracer/1.0

v=0
o={from_phone} {int(time.time())} {int(time.time())} IN IP4 {from_ip}
s=VoIP Call
c=IN IP4 {from_ip}
t=0 0
m=audio {random.randint(10000, 60000)} RTP/AVP 0 8 18
a=rtpmap:0 PCMU/8000
a=rtpmap:8 PCMA/8000
a=rtpmap:18 G729/8000
"""
        return sip_msg.encode()

    def create_sip_response(self, code, phrase, from_phone, to_phone, from_ip, to_ip, call_id):
        """Create SIP response message"""
        sip_msg = f"""SIP/2.0 {code} {phrase}
Via: SIP/2.0/UDP {from_ip}:5060;branch=z9hG4bK{random.randint(100000, 999999)}
To: <sip:{to_phone}@{to_ip}>;tag={random.randint(100000, 999999)}
From: "{from_phone}" <sip:{from_phone}@{from_ip}>;tag={random.randint(100000, 999999)}
Call-ID: {call_id}@{from_ip}
CSeq: 1 INVITE
Content-Length: 0

"""
        return sip_msg.encode()

    def create_rtp_packet(self, payload_type=0, sequence=None, timestamp=None, ssrc=None):
        """Create RTP packet"""
        if sequence is None:
            sequence = random.randint(1000, 65535)
        if timestamp is None:
            timestamp = random.randint(1000000, 4000000000)
        if ssrc is None:
            ssrc = random.randint(1000000, 4000000000)
        
        # RTP header
        version = 2
        padding = 0
        extension = 0
        cc = 0
        marker = random.choice([0, 1])
        
        rtp_header = struct.pack('>BBHLL',
            (version << 6) | (padding << 5) | (extension << 4) | cc,
            (marker << 7) | payload_type,
            sequence,
            timestamp,
            ssrc
        )
        
        # Generate audio payload (simulated)
        payload_size = random.randint(20, 160)
        payload = bytes([random.randint(0, 255) for _ in range(payload_size)])
        
        return rtp_header + payload

    def create_anomaly_traffic(self, anomaly_type):
        """Create anomalous traffic patterns"""
        anomalies = []
        
        if anomaly_type == 'brute_force':
            # SIP brute force attack
            attacker_ip = self.generate_ip('suspicious')
            target_ip = self.generate_ip('voip_servers')
            
            for i in range(50):  # 50 rapid attempts
                fake_user = f"user{random.randint(1000, 9999)}"
                call_id = f"attack-{random.randint(100000, 999999)}"
                
                sip_msg = f"""REGISTER sip:{target_ip} SIP/2.0
Via: SIP/2.0/UDP {attacker_ip}:5060
To: <sip:{fake_user}@{target_ip}>
From: <sip:{fake_user}@{target_ip}>
Call-ID: {call_id}@{attacker_ip}
CSeq: {i+1} REGISTER
Authorization: Digest username="{fake_user}", password="admin123"
Content-Length: 0

""".encode()
                
                anomalies.append({
                    'src_ip': attacker_ip,
                    'dst_ip': target_ip,
                    'src_port': 5060,
                    'dst_port': 5060,
                    'payload': sip_msg,
                    'timestamp': time.time() + i * 0.1
                })
        
        elif anomaly_type == 'call_flooding':
            # Excessive call attempts
            attacker_ip = self.generate_ip('suspicious')
            target_number = self.generate_phone_number()
            
            for i in range(100):  # 100 calls in short time
                call_id = f"flood-{random.randint(100000, 999999)}"
                attacker_number = self.generate_phone_number('suspicious')
                
                sip_msg = self.create_sip_invite(
                    attacker_number, target_number,
                    attacker_ip, self.generate_ip('voip_servers'),
                    call_id
                )
                
                anomalies.append({
                    'src_ip': attacker_ip,
                    'dst_ip': self.generate_ip('voip_servers'),
                    'src_port': random.randint(5060, 5070),
                    'dst_port': 5060,
                    'payload': sip_msg,
                    'timestamp': time.time() + i * 0.05
                })
        
        elif anomaly_type == 'codec_manipulation':
            # Unusual codec negotiation
            for i in range(20):
                from_ip = self.generate_ip('suspicious')
                to_ip = self.generate_ip('voip_servers')
                
                # Use unusual payload types
                rtp_data = self.create_rtp_packet(payload_type=random.randint(110, 127))
                
                anomalies.append({
                    'src_ip': from_ip,
                    'dst_ip': to_ip,
                    'src_port': random.randint(10000, 60000),
                    'dst_port': random.randint(10000, 60000),
                    'payload': rtp_data,
                    'timestamp': time.time() + i * 2
                })
        
        return anomalies

    def write_packet(self, file_handle, src_ip, dst_ip, src_port, dst_port, payload, timestamp=None):
        """Write a complete packet to PCAP file"""
        if timestamp is None:
            timestamp = time.time()
        
        # Create headers
        eth_header = self.create_ethernet_header()
        ip_header = self.create_ip_header(src_ip, dst_ip, 8 + len(payload))
        udp_header = self.create_udp_header(src_port, dst_port, len(payload))
        
        # Complete packet
        packet = eth_header + ip_header + udp_header + payload
        
        # PCAP record header
        ts_sec = int(timestamp)
        ts_usec = int((timestamp - ts_sec) * 1000000)
        incl_len = len(packet)
        orig_len = len(packet)
        
        record_header = struct.pack('<LLLL', ts_sec, ts_usec, incl_len, orig_len)
        
        file_handle.write(record_header + packet)

    def generate_large_diverse_pcap(self, filename, num_calls=1000, include_anomalies=True):
        """Generate large PCAP file with diverse VoIP traffic"""
        print(f"Generating diverse PCAP: {filename}")
        print(f"Target calls: {num_calls}")
        
        with open(filename, 'wb') as f:
            # Write PCAP header
            f.write(self.pcap_header)
            
            call_sessions = []
            base_time = time.time()
            
            # Generate normal call sessions
            print("Generating normal call traffic...")
            for i in range(num_calls):
                # Create diverse call scenarios
                scenario = random.choice([
                    'internal_call', 'external_call', 'international_call',
                    'conference_call', 'mobile_call', 'voicemail'
                ])
                
                if scenario == 'internal_call':
                    from_ip = self.generate_ip('internal')
                    to_ip = self.generate_ip('internal')
                elif scenario == 'external_call':
                    from_ip = self.generate_ip('internal')
                    to_ip = self.generate_ip('external')
                elif scenario == 'international_call':
                    from_ip = self.generate_ip('internal')
                    to_ip = self.generate_ip('external')
                else:
                    from_ip = self.generate_ip('internal')
                    to_ip = self.generate_ip('voip_servers')
                
                from_phone = self.generate_phone_number()
                to_phone = self.generate_phone_number()
                call_id = f"call-{i:06d}-{random.randint(100000, 999999)}"
                
                # Call duration (2-300 seconds)
                call_duration = random.randint(2, 300)
                call_start_time = base_time + i * random.uniform(0.1, 5.0)
                
                # SIP signaling
                invite_payload = self.create_sip_invite(from_phone, to_phone, from_ip, to_ip, call_id)
                self.write_packet(f, from_ip, to_ip, 5060, 5060, invite_payload, call_start_time)
                
                # Response (with some failures for realism)
                response_code = random.choices([200, 180, 486, 404], weights=[70, 15, 10, 5])[0]
                response_payload = self.create_sip_response(
                    response_code, self.sip_responses[response_code],
                    from_phone, to_phone, to_ip, from_ip, call_id
                )
                self.write_packet(f, to_ip, from_ip, 5060, 5060, response_payload, call_start_time + 0.5)
                
                # If call successful, generate RTP traffic
                if response_code == 200:
                    rtp_from_port = random.randint(10000, 60000)
                    rtp_to_port = random.randint(10000, 60000)
                    
                    # Generate RTP packets for call duration
                    packet_interval = 0.02  # 20ms intervals
                    num_rtp_packets = int(call_duration / packet_interval)
                    
                    for j in range(min(num_rtp_packets, 500)):  # Limit packets per call
                        # Bidirectional RTP
                        rtp_time = call_start_time + 1.0 + j * packet_interval
                        
                        # From -> To
                        rtp_payload = self.create_rtp_packet(
                            payload_type=random.choice([0, 8, 18]),
                            sequence=j + 1000,
                            timestamp=int(rtp_time * 8000) % (2**32)
                        )
                        self.write_packet(f, from_ip, to_ip, rtp_from_port, rtp_to_port, rtp_payload, rtp_time)
                        
                        # To -> From (every other packet for efficiency)
                        if j % 2 == 0:
                            rtp_payload_back = self.create_rtp_packet(
                                payload_type=random.choice([0, 8, 18]),
                                sequence=j + 2000,
                                timestamp=int(rtp_time * 8000) % (2**32)
                            )
                            self.write_packet(f, to_ip, from_ip, rtp_to_port, rtp_from_port, rtp_payload_back, rtp_time + 0.01)
                    
                    # BYE message
                    bye_payload = f"""BYE sip:{to_phone}@{to_ip} SIP/2.0
Via: SIP/2.0/UDP {from_ip}:5060
To: <sip:{to_phone}@{to_ip}>
From: <sip:{from_phone}@{from_ip}>
Call-ID: {call_id}@{from_ip}
CSeq: 2 BYE
Content-Length: 0

""".encode()
                    self.write_packet(f, from_ip, to_ip, 5060, 5060, bye_payload, call_start_time + call_duration)
                
                if (i + 1) % 100 == 0:
                    print(f"Generated {i + 1} calls...")
            
            # Add anomalous traffic
            if include_anomalies:
                print("Adding anomalous traffic patterns...")
                
                anomaly_types = ['brute_force', 'call_flooding', 'codec_manipulation']
                for anomaly_type in anomaly_types:
                    print(f"  Adding {anomaly_type} anomalies...")
                    anomalies = self.create_anomaly_traffic(anomaly_type)
                    
                    for anomaly in anomalies:
                        self.write_packet(
                            f, anomaly['src_ip'], anomaly['dst_ip'],
                            anomaly['src_port'], anomaly['dst_port'],
                            anomaly['payload'], base_time + anomaly['timestamp']
                        )
        
        # Get file size
        import os
        file_size = os.path.getsize(filename)
        print(f"Generated {filename}")
        print(f"File size: {file_size / (1024*1024):.2f} MB")
        print(f"Contains: {num_calls} call sessions + anomalies")

def main():
    generator = EnhancedPCAPGenerator()
    
    # Generate different types of PCAP files
    pcap_files = [
        ('enterprise_voip_large.pcap', 2000, True),
        ('international_calls.pcap', 500, False),
        ('suspicious_activity.pcap', 100, True),
    ]
    
    for filename, num_calls, include_anomalies in pcap_files:
        generator.generate_large_diverse_pcap(filename, num_calls, include_anomalies)
        print("-" * 50)

if __name__ == "__main__":
    main()
