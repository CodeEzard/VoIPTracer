from http.server import BaseHTTPRequestHandler
import json
import random
import time
from datetime import datetime, timedelta

class handler(BaseHTTPRequestHandler):
    def generate_realistic_data(self):
        """Generate realistic VoIP analysis data"""
        # Random number of calls (10-50 for demo)
        num_calls = random.randint(15, 45)
        
        # Phone number prefixes for variety
        prefixes = ['+1415', '+1212', '+1310', '+44207', '+3312', '+4930', '+91124']
        domains = ['enterprise.com', 'techcorp.net', 'voipservice.org', 'company.biz', 'telecom.co']
        
        calls = []
        total_duration = 0
        total_packets = 0
        anomaly_count = 0
        
        for i in range(num_calls):
            # Generate diverse call data
            from_number = random.choice(prefixes) + ''.join([str(random.randint(0, 9)) for _ in range(7)])
            to_number = random.choice(prefixes) + ''.join([str(random.randint(0, 9)) for _ in range(7)])
            from_domain = random.choice(domains)
            to_domain = random.choice(domains)
            
            # Call characteristics
            duration = round(random.uniform(5.0, 300.0), 1)  # 5 seconds to 5 minutes
            packets = random.randint(int(duration * 2), int(duration * 8))  # Realistic packet count
            
            # Anomaly detection (15-25% chance)
            is_anomaly = random.random() < 0.2
            if is_anomaly:
                anomaly_count += 1
                # Anomalous calls might be shorter or have unusual packet counts
                if random.choice([True, False]):
                    duration = random.uniform(0.5, 3.0)  # Very short calls
                else:
                    packets = int(packets * random.uniform(0.1, 0.3))  # Low packet count
            
            call = {
                "call_id": f"demo-call-{i+1:03d}",
                "from_uri": f"sip:{from_number}@{from_domain}",
                "to_uri": f"sip:{to_number}@{to_domain}",
                "duration": duration,
                "duration_s": duration,  # Frontend expects this
                "packets": packets,
                "total_pkts": packets,  # Frontend expects this
                "anomaly": is_anomaly,
                "is_anomaly": is_anomaly,  # Frontend expects this
                "anomaly_score": round(random.uniform(0.8, 0.99), 3) if is_anomaly else round(random.uniform(0.0, 0.3), 3),
                "codec": random.choice(['PCMU', 'PCMA', 'G729', 'iLBC', 'Opus']),
                "jitter": round(random.uniform(0.1, 15.0), 2),
                "packet_loss": round(random.uniform(0.0, 5.0), 2),
                "num_dst_ips": random.randint(1, 5),
                "source_ip": f"192.168.{random.randint(1,254)}.{random.randint(1,254)}",
                "dest_ip": f"10.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
            }
            
            calls.append(call)
            total_duration += duration
            total_packets += packets
        
        return {
            "calls": calls,
            "summary": {
                "total_calls": num_calls,
                "anomalies": anomaly_count,
                "anomaly_rate": round(anomaly_count / num_calls, 3)
            },
            "stats": {
                "total_calls": num_calls,
                "anomaly_count": anomaly_count,
                "total_packets": total_packets,
                "total_duration": round(total_duration, 1),
                "avg_duration": round(total_duration / num_calls, 1),
                "avg_packets_per_call": round(total_packets / num_calls, 1)
            },
            "message": "Demo analysis completed with realistic data simulation",
            "packets_processed": total_packets,
            "analysis_time": round(random.uniform(1.5, 4.2), 2),
            "timestamp": datetime.now().isoformat()
        }

    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

            # Generate dynamic realistic data
            response = self.generate_realistic_data()
            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            error_response = {
                "error": f"Demo analysis failed: {str(e)}",
                "calls": [],
                "summary": {"total_calls": 0, "anomalies": 0, "anomaly_rate": 0.0}
            }
            self.wfile.write(json.dumps(error_response).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
