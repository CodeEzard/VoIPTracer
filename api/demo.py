from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from capture import read_pcap
    from parser import attach_meta_from_raw_packets
    from agg import calls_to_dataframe, add_derived_features
    from analyze import detect_anomalies
except ImportError as e:
    print(f"Import error: {e}")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

            # Use the existing demo pcap file
            demo_pcap_path = os.path.join(os.path.dirname(__file__), '..', 'large_diverse_voip_traffic.pcap')
            
            if not os.path.exists(demo_pcap_path):
                # Fallback response if demo file not found
                response = {
                    "calls": [
                        {
                            "call_id": "demo-call-1",
                            "from_uri": "sip:alice@example.com",
                            "to_uri": "sip:bob@example.com",
                            "duration": 45.2,
                            "packets": 120,
                            "anomaly": False
                        },
                        {
                            "call_id": "demo-call-2", 
                            "from_uri": "sip:charlie@example.com",
                            "to_uri": "sip:diana@example.com",
                            "duration": 12.8,
                            "packets": 35,
                            "anomaly": True
                        },
                        {
                            "call_id": "demo-call-3",
                            "from_uri": "sip:eve@example.com", 
                            "to_uri": "sip:frank@example.com",
                            "duration": 89.1,
                            "packets": 245,
                            "anomaly": False
                        }
                    ],
                    "summary": {
                        "total_calls": 3,
                        "anomalies": 1,
                        "anomaly_rate": 0.33
                    },
                    "stats": {
                        "total_calls": 3,
                        "anomaly_count": 1,
                        "total_packets": 400,
                        "total_duration": 147.1
                    },
                    "message": "Demo analysis completed (fallback data)",
                    "packets_processed": 400
                }
            else:
                # Process actual demo file
                packets = list(read_pcap(demo_pcap_path, limit=100))  # Limit for serverless
                calls = attach_meta_from_raw_packets(packets)
                
                if not calls:
                    response = {
                        "calls": [],
                        "summary": {
                            "total_calls": 0,
                            "anomalies": 0,
                            "anomaly_rate": 0.0
                        },
                        "stats": {
                            "total_calls": 0,
                            "anomaly_count": 0,
                            "total_packets": len(packets),
                            "total_duration": 0.0
                        },
                        "message": "No VoIP calls detected in demo file",
                        "packets_processed": len(packets)
                    }
                else:
                    df = calls_to_dataframe(calls)
                    df = add_derived_features(df)
                    df = detect_anomalies(df)
                    
                    anomaly_count = df['anomaly'].sum() if 'anomaly' in df.columns else 0
                    total_calls = len(df)
                    
                    response = {
                        "calls": df.to_dict('records'),
                        "summary": {
                            "total_calls": total_calls,
                            "anomalies": int(anomaly_count),
                            "anomaly_rate": float(anomaly_count / total_calls) if total_calls > 0 else 0.0
                        },
                        "stats": {
                            "total_calls": total_calls,
                            "anomaly_count": int(anomaly_count),
                            "total_packets": len(packets),
                            "total_duration": float(df['duration'].sum()) if 'duration' in df.columns else 0.0
                        },
                        "message": f"Demo analysis completed - {total_calls} calls found",
                        "packets_processed": len(packets)
                    }

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
        return
