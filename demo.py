#!/usr/bin/env python3
"""
Demo script for VoIP Meta Tracer
Shows how to use the complete pipeline
"""

import sys
import os
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src import capture, parser, agg, analyze, viz

def demo_voip_analysis():
    """Demonstrate the complete VoIP analysis pipeline."""
    
    print("🎯 VoIP Meta Tracer Demo")
    print("=" * 50)
    
    # Simulate some VoIP traffic data
    print("\n1. Simulating VoIP packet capture...")
    mock_packets = [
        {
            'ts': 1234567890.1,
            'proto': 'SIP',
            'src_ip': '192.168.1.100',
            'dst_ip': '10.0.1.50',
            'src_port': 5060,
            'dst_port': 5060,
            'call_id': 'suspicious-call-001',
            'from_uri': 'INVITE sip:target@company.com',
            'to_uri': 'sip:target@company.com',
            'pkt_len': 800,
            'ssrc': 0,
            'ja3': ''
        },
        {
            'ts': 1234567890.2,
            'proto': 'RTP',
            'src_ip': '192.168.1.100',
            'dst_ip': '10.0.1.50',
            'src_port': 8000,
            'dst_port': 8001,
            'ssrc': 11111111,
            'call_id': '',
            'from_uri': '',
            'to_uri': '',
            'pkt_len': 200,
            'ja3': ''
        },
        {
            'ts': 1234567892.0,
            'proto': 'SIP',
            'src_ip': '10.0.1.25',
            'dst_ip': '192.168.2.100',
            'src_port': 5060,
            'dst_port': 5060,
            'call_id': 'normal-call-002',
            'from_uri': 'INVITE sip:alice@office.com',
            'to_uri': 'sip:bob@office.com',
            'pkt_len': 450,
            'ssrc': 0,
            'ja3': ''
        },
        {
            'ts': 1234567892.1,
            'proto': 'RTP',
            'src_ip': '10.0.1.25',
            'dst_ip': '192.168.2.100',
            'src_port': 8002,
            'dst_port': 8003,
            'ssrc': 22222222,
            'call_id': '',
            'from_uri': '',
            'to_uri': '',
            'pkt_len': 200,
            'ja3': ''
        },
        # Add some suspicious rapid calls
        {
            'ts': 1234567895.0,
            'proto': 'SIP',
            'src_ip': '192.168.1.100',
            'dst_ip': '203.0.113.50',  # External IP
            'src_port': 5060,
            'dst_port': 5060,
            'call_id': 'rapid-call-003',
            'from_uri': 'INVITE sip:victim@target.com',
            'to_uri': 'sip:victim@target.com',
            'pkt_len': 900,
            'ssrc': 0,
            'ja3': ''
        },
        {
            'ts': 1234567895.5,
            'proto': 'SIP',
            'src_ip': '192.168.1.100',
            'dst_ip': '203.0.113.51',  # Another external IP
            'src_port': 5060,
            'dst_port': 5060,
            'call_id': 'rapid-call-004',
            'from_uri': 'INVITE sip:victim2@target.com',
            'to_uri': 'sip:victim2@target.com',
            'pkt_len': 950,
            'ssrc': 0,
            'ja3': ''
        }
    ]
    print(f"   📦 Captured {len(mock_packets)} packets")
    
    # Parse calls
    print("\n2. Parsing and grouping calls...")
    calls = parser.attach_meta_from_raw_packets(mock_packets)
    print(f"   📞 Identified {len(calls)} call sessions:")
    for call_id, call_data in calls.items():
        print(f"      - {call_id}: {call_data['total_pkts']} packets, "
              f"{call_data['duration_s']:.1f}s duration")
    
    # Convert to DataFrame for analysis
    print("\n3. Converting to DataFrame for ML analysis...")
    df = agg.calls_to_dataframe(calls)
    df = agg.add_derived_features(df)  # Add derived features for ML
    print(f"   📊 DataFrame: {len(df)} rows × {len(df.columns)} columns")
    print(f"   📈 Features: {list(df.columns)}")
    
    # Perform anomaly detection
    print("\n4. Running anomaly detection...")
    df_with_anomalies = analyze.detect_anomalies(df)
    if 'is_anomaly' in df_with_anomalies.columns:
        anomaly_count = df_with_anomalies['is_anomaly'].sum()
        print(f"   🚨 Detected {anomaly_count} anomalous calls:")
        
        if anomaly_count > 0:
            anomalous_calls = df_with_anomalies[df_with_anomalies['is_anomaly']]
            for idx, row in anomalous_calls.iterrows():
                print(f"      ⚠️  Call {row['call_id']}: "
                      f"{row['total_pkts']} packets, "
                      f"{row.get('num_dst_ips', 'N/A')} destinations")
    else:
        print("   ℹ️  Anomaly detection skipped (insufficient data)")
    
    # Flag suspicious patterns
    print("\n5. Checking for suspicious patterns...")
    df_flagged = analyze.flag_suspicious_patterns(df_with_anomalies)
    patterns_found = []
    
    for pattern in ['flag_short_burst', 'flag_no_rtp', 'flag_high_diversity', 'flag_unusual_time', 'flag_large_packets']:
        if pattern in df_flagged.columns and df_flagged[pattern].any():
            count = df_flagged[pattern].sum()
            patterns_found.append(f"{pattern.replace('flag_', '')}: {count}")
    
    if patterns_found:
        print(f"   🔍 Suspicious patterns found: {', '.join(patterns_found)}")
    else:
        print("   ✅ No suspicious patterns detected")
    
    # Build call graph
    print("\n6. Building call relationship graph...")
    try:
        graph = viz.build_call_graph(calls)
        print(f"   🕸️  Graph: {len(graph.nodes)} nodes, {len(graph.edges)} edges")
        
        # Show some graph stats
        if len(graph.nodes) > 0:
            from collections import Counter
            degree_counts = Counter([graph.degree(n) for n in graph.nodes()])
            print(f"   📈 Node degrees: {dict(degree_counts)}")
            
    except Exception as e:
        print(f"   ⚠️  Graph build failed: {e}")
    
    # Export results
    print("\n7. Exporting results...")
    try:
        # Export to CSV
        output_file = "voip_analysis_results.csv"
        viz.export_csv(df_flagged, output_file)
        print(f"   💾 Results saved to: {output_file}")
        
        # Export call metadata as JSON
        with open("call_metadata.json", 'w') as f:
            json.dump(calls, f, indent=2, default=str)
        print(f"   💾 Call metadata saved to: call_metadata.json")
        
    except Exception as e:
        print(f"   ⚠️  Export failed: {e}")
    
    # Calculate final stats
    anomaly_count = df_flagged['is_anomaly'].sum() if 'is_anomaly' in df_flagged.columns else 0
    
    print("\n🎉 Demo completed!")
    print("\n" + "=" * 50)
    print("VoIP Meta Tracer Analysis Summary:")
    print(f"• Processed {len(mock_packets)} packets")
    print(f"• Identified {len(calls)} call sessions")
    print(f"• Detected {anomaly_count} anomalies")
    print(f"• Found {len(patterns_found)} suspicious patterns")
    print("• Generated call relationship graph")
    print("• Exported results to CSV and JSON")
    
    return True

if __name__ == "__main__":
    demo_voip_analysis()
