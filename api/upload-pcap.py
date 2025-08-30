from http.server import BaseHTTPRequestHandler
import json
import sys
import os
import tempfile
import cgi
from io import BytesIO

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from serverless_capture import read_pcap_simple, extract_simple_calls
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback imports
    def read_pcap_simple(path, limit=50):
        return []
    def extract_simple_calls(packets):
        return []

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

            # Read the POST data
            post_data = self.rfile.read(content_length)
            
            # Parse form data
            form_data = cgi.FieldStorage(
                fp=BytesIO(post_data),
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            # Get the uploaded file
            if 'file' not in form_data:
                self.wfile.write(json.dumps({"error": "No file field found"}).encode())
                return

            file_item = form_data['file']
            if not file_item.filename:
                self.wfile.write(json.dumps({"error": "No file selected"}).encode())
                return

            # Save file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pcap') as temp_file:
                temp_file.write(file_item.file.read())
                temp_file_path = temp_file.name

            try:
                # Process the PCAP file (simplified for serverless)
                packets = read_pcap_simple(temp_file_path, limit=100)  # Limit for serverless
                calls = extract_simple_calls(packets)
                
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
                        "message": "No VoIP calls detected in PCAP file",
                        "packets_processed": len(packets)
                    }
                else:
                    # Simple anomaly detection based on packet count
                    total_calls = len(calls)
                    anomaly_count = sum(1 for call in calls if call.get('packets', 0) > 50 or call.get('packets', 0) < 5)
                    
                    # Mark anomalies
                    for call in calls:
                        call['anomaly'] = call.get('packets', 0) > 50 or call.get('packets', 0) < 5
                    
                    response = {
                        "calls": calls,
                        "summary": {
                            "total_calls": total_calls,
                            "anomalies": anomaly_count,
                            "anomaly_rate": float(anomaly_count / total_calls) if total_calls > 0 else 0.0
                        },
                        "stats": {
                            "total_calls": total_calls,
                            "anomaly_count": anomaly_count,
                            "total_packets": len(packets),
                            "total_duration": sum(call.get('duration', 0) for call in calls)
                        },
                        "message": f"Successfully analyzed {total_calls} calls",
                        "packets_processed": len(packets)
                    }

            finally:
                # Clean up temp file
                os.unlink(temp_file_path)

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
        return
