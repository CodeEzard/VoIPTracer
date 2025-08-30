from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

            # Return demo data without complex dependencies
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
                "message": "Demo analysis completed successfully",
                "packets_processed": 400
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
