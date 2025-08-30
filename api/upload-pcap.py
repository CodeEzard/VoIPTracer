from http.server import BaseHTTPRequestHandler
import json
import tempfile
import cgi
from io import BytesIO

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Handle CORS
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

            # Parse multipart form data
            content_type = self.headers.get('Content-Type', '')
            if not content_type.startswith('multipart/form-data'):
                self.wfile.write(json.dumps({"error": "Expected multipart/form-data"}).encode())
                return

            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.wfile.write(json.dumps({"error": "No file uploaded"}).encode())
                return

            # For demo purposes, return mock analysis results
            # In a real serverless environment, PCAP processing would be complex
            response = {
                "calls": [
                    {
                        "call_id": "uploaded-call-1",
                        "from_uri": "sip:user1@uploaded.com",
                        "to_uri": "sip:user2@uploaded.com",
                        "duration": 32.5,
                        "packets": 89,
                        "anomaly": False
                    },
                    {
                        "call_id": "uploaded-call-2",
                        "from_uri": "sip:user3@uploaded.com", 
                        "to_uri": "sip:user4@uploaded.com",
                        "duration": 156.2,
                        "packets": 420,
                        "anomaly": True
                    }
                ],
                "summary": {
                    "total_calls": 2,
                    "anomalies": 1,
                    "anomaly_rate": 0.5
                },
                "stats": {
                    "total_calls": 2,
                    "anomaly_count": 1,
                    "total_packets": 509,
                    "total_duration": 188.7
                },
                "message": "PCAP file analysis completed (demo mode)",
                "packets_processed": 509
            }

            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            error_response = {
                "error": f"Analysis failed: {str(e)}",
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
