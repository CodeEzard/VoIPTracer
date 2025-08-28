"""Basic smoke tests for the VoIP metadata tracer."""

import pytest
import tempfile
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Mock data for testing since we don't have real pcap files
MOCK_PACKETS = [
    {
        'ts': 1234567890.0,
        'src_ip': '10.0.0.1',
        'dst_ip': '10.0.0.2',
        'proto': 'SIP',
        'call_id': 'test-call-123',
        'from_uri': 'sip:alice@example.com',
        'to_uri': 'sip:bob@example.com',
        'ssrc': 0,
        'pkt_len': 500,
        'tls_ver': '',
        'ja3': ''
    },
    {
        'ts': 1234567891.0,
        'src_ip': '10.0.0.1',
        'dst_ip': '10.0.0.2',
        'proto': 'RTP',
        'call_id': '',
        'from_uri': '',
        'to_uri': '',
        'ssrc': 12345,
        'pkt_len': 200,
        'tls_ver': '',
        'ja3': ''
    },
    {
        'ts': 1234567892.0,
        'src_ip': '10.0.0.1',
        'dst_ip': '10.0.0.2',
        'proto': 'RTP',
        'call_id': '',
        'from_uri': '',
        'to_uri': '',
        'ssrc': 12345,
        'pkt_len': 200,
        'tls_ver': '',
        'ja3': ''
    }
]


def test_parser_attach_meta():
    """Test parser functionality with mock data."""
    from src import parser
    
    calls = parser.attach_meta_from_raw_packets(MOCK_PACKETS)
    
    assert len(calls) == 2  # One SIP call + one RTP session
    assert 'test-call-123' in calls
    assert calls['test-call-123']['sip_pkts'] == 1
    assert calls['test-call-123']['from_uri'] == 'sip:alice@example.com'


def test_agg_calls_to_dataframe():
    """Test DataFrame conversion."""
    from src import parser, agg
    
    calls = parser.attach_meta_from_raw_packets(MOCK_PACKETS)
    df = agg.calls_to_dataframe(calls)
    
    assert len(df) == 2
    assert 'duration_s' in df.columns
    assert 'total_pkts' in df.columns
    
    # Test derived features
    df = agg.add_derived_features(df)
    assert 'pkts_per_sec' in df.columns
    assert 'rtp_ratio' in df.columns


def test_analyze_anomalies():
    """Test anomaly detection."""
    from src import parser, agg, analyze
    
    calls = parser.attach_meta_from_raw_packets(MOCK_PACKETS)
    df = agg.calls_to_dataframe(calls)
    df = agg.add_derived_features(df)
    
    # With only 2 calls, anomaly detection should still work
    df = analyze.detect_anomalies(df, contamination=0.5)
    assert 'anomaly_score' in df.columns
    assert 'is_anomaly' in df.columns
    
    # Test suspicious patterns
    df = analyze.flag_suspicious_patterns(df)
    flag_cols = [col for col in df.columns if col.startswith('flag_')]
    assert len(flag_cols) > 0


def test_viz_build_graph():
    """Test graph building."""
    from src import parser, agg, viz
    
    calls = parser.attach_meta_from_raw_packets(MOCK_PACKETS)
    df = agg.calls_to_dataframe(calls)
    
    graph = viz.build_call_graph(df)
    assert len(graph.nodes) >= 2  # At least source and dest IPs
    assert len(graph.edges) >= 1


def test_pipeline_integration():
    """Test full pipeline integration."""
    from src import parser, agg, analyze, viz
    
    # Mock the full pipeline
    calls = parser.attach_meta_from_raw_packets(MOCK_PACKETS)
    df = agg.calls_to_dataframe(calls)
    df = agg.add_derived_features(df)
    df = agg.filter_calls(df, min_duration=0.0, min_pkts=1)
    df = analyze.detect_anomalies(df)
    df = analyze.flag_suspicious_patterns(df)
    
    summary = analyze.summarize_anomalies(df)
    assert 'total_calls' in summary
    assert summary['total_calls'] > 0
    
    # Test export functions don't crash
    with tempfile.TemporaryDirectory() as tmp_dir:
        csv_path = os.path.join(tmp_dir, "test.csv")
        viz.export_csv(df, csv_path)
        assert os.path.exists(csv_path)


if __name__ == "__main__":
    # Run tests directly
    test_parser_attach_meta()
    test_agg_calls_to_dataframe()
    test_analyze_anomalies()
    test_viz_build_graph()
    test_pipeline_integration()
    print("All tests passed!")
