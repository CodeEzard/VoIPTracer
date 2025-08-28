# VoIP Meta Tracer

An end-to-end Python project for analyzing VoIP metadata from packet captures without decrypting SRTP/TLS traffic.

## Features

- **Packet Analysis**: Extract SIP, RTP, and TLS/DTLS metadata from pcap files
- **Call Grouping**: Group packets by call-id and SSRC for session reconstruction
- **Anomaly Detection**: Use ML (IsolationForest) to detect suspicious call patterns
- **Visualization**: Generate network graphs and export CSV reports
- **REST API**: FastAPI endpoint for uploading pcaps and getting analysis results
- **Live Capture**: Support for real-time packet analysis (pyshark.LiveCapture)

## Quick Start

### Prerequisites

- Python 3.10+
- tshark/Wireshark (for pyshark packet analysis)
- Git (for cloning the repository)

### Installation

```bash
git clone <repo-url>
cd voip-meta-tracer
pip install -r requirements.txt
```

### Basic Usage

```python
from src import capture, parser, agg, analyze, viz

# Analyze a pcap file
packets = list(capture.read_pcap("data/sample.pcap", limit=1000))
calls = parser.attach_meta_from_raw_packets(packets)
df = agg.calls_to_dataframe(calls)
df = agg.add_derived_features(df)
df = analyze.detect_anomalies(df)

# Export results
viz.export_csv(df, "out/calls.csv")
graph = viz.build_call_graph(df)
viz.plot_call_graph(graph, "out/graph.png")
```

### API Server

```bash
# Start the API server
python -m uvicorn src.api:app --host 0.0.0.0 --port 8000

# Upload a pcap for analysis
curl -X POST "http://localhost:8000/upload-pcap" \
     -F "file=@sample.pcap" \
     -F "limit=1000"
```

### Docker

```bash
# Build and run
docker build -t voip-meta-tracer .
docker run -p 8000:8000 voip-meta-tracer

# Test
curl http://localhost:8000/
```

## Project Structure

```
voip-meta-tracer/
├── src/
│   ├── capture.py    # Extract metadata from pcap/live traffic
│   ├── parser.py     # Group packets by call, extract SDP/JA3
│   ├── agg.py        # Convert to DataFrame, add features
│   ├── analyze.py    # Anomaly detection with IsolationForest
│   ├── viz.py        # CSV export, graph visualization
│   └── api.py        # FastAPI endpoints
├── tests/
│   └── test_smoke.py # Basic integration tests
├── data/             # Sample pcap files
├── out/              # Output CSV and graphs
├── requirements.txt
├── Dockerfile
└── .github/workflows/ci.yml
```

## Metadata Extracted

### SIP Packets
- Call-ID, From URI, To URI
- SDP fingerprints (`a=fingerprint`)
- Method, response codes

### RTP Packets
- SSRC, packet count, timestamps
- Payload type, sequence numbers

### TLS/DTLS Packets
- Handshake version
- JA3 fingerprints (stub implementation)
- Certificate metadata

## Anomaly Detection

The system flags calls as anomalous based on:

- **Statistical outliers**: Duration, packet count, byte volume
- **Behavioral patterns**: 
  - Short bursts (many packets, short duration)
  - Missing RTP (SIP without media)
  - High IP diversity (potential relay abuse)
  - Off-hours activity
  - Unusually large packets

## Development

### Running Tests

```bash
# With pytest
python -m pytest tests/ -v

# Direct execution
cd tests && python test_smoke.py
```

### Next Features

- [ ] Live capture mode integration
- [ ] GeoIP enrichment with `geoip2`
- [ ] Web dashboard (React/Next.js)
- [ ] Real JA3 fingerprinting
- [ ] SDP parsing for media capabilities
- [ ] RTCP analysis
- [ ] Call quality metrics

## API Endpoints

- `GET /` - Health check
- `POST /upload-pcap` - Upload pcap file for analysis
- `POST /analyze-file` - Analyze existing file on server

## Configuration

Environment variables:
- `PYTHONPATH` - Set to project root
- `LOG_LEVEL` - Logging verbosity (default: INFO)

## License

MIT License - see LICENSE file for details.
