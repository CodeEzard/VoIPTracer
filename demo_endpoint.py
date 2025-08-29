
@app.get("/demo")
async def demo_analysis():
    """Run demo analysis with sample data."""
    try:
        # Import required modules
        from . import capture, parser, agg, analyze, viz
        
        # Create sample VoIP data
        mock_packets = [
            {
                'ts': 1234567890.1, 'proto': 'SIP', 'src_ip': '192.168.1.100',
                'dst_ip': '10.0.1.50', 'src_port': 5060, 'dst_port': 5060,
                'call_id': 'demo-call-001', 'from_uri': 'sip:alice@demo.com', 'to_uri': 'sip:bob@demo.com',
                'pkt_len': 450, 'ssrc': 0, 'ja3': ''
            },
            {
                'ts': 1234567890.5, 'proto': 'RTP', 'src_ip': '192.168.1.100',
                'dst_ip': '10.0.1.50', 'src_port': 8000, 'dst_port': 8001,
                'call_id': '', 'from_uri': '', 'to_uri': '',
                'pkt_len': 200, 'ssrc': 11111111, 'ja3': ''
            },
            {
                'ts': 1234567892.0, 'proto': 'SIP', 'src_ip': '192.168.1.200',
                'dst_ip': '203.0.113.50', 'src_port': 5060, 'dst_port': 5060,
                'call_id': 'suspicious-call-002', 'from_uri': 'sip:attacker@malicious.com', 'to_uri': 'sip:victim@target.com',
                'pkt_len': 800, 'ssrc': 0, 'ja3': ''
            }
        ]
        
        # Process through the pipeline
        calls = parser.attach_meta_from_raw_packets(mock_packets)
        df = agg.calls_to_dataframe(calls)
        df = agg.add_derived_features(df)
        df_anomalies = analyze.detect_anomalies(df)
        df_flagged = analyze.flag_suspicious_patterns(df_anomalies)
        
        # Convert to JSON-serializable format
        results = df_flagged.to_dict('records')
        
        # Calculate stats
        stats = {
            "total_calls": len(results),
            "anomaly_count": sum(1 for call in results if call.get('is_anomaly', False)),
            "total_packets": sum(call.get('total_pkts', 0) for call in results),
            "total_duration": sum(call.get('duration_s', 0) for call in results)
        }
        
        return {
            "calls": results,
            "stats": stats,
            "message": "Demo analysis completed successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo analysis failed: {str(e)}")

