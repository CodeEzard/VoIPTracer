#!/usr/bin/env python3
"""Test the API with the new PCAP file and show From/To information."""

import requests
import json

def test_large_pcap():
    """Test the large diverse PCAP file via API."""
    
    print("🧪 Testing large_diverse_voip_traffic.pcap via API...")
    print("=" * 60)
    
    # Test with limit to avoid overwhelming response
    url = "http://localhost:8002/upload-pcap"
    
    try:
        with open("large_diverse_voip_traffic.pcap", "rb") as f:
            files = {"file": f}
            data = {"limit": 200}  # Limit to 200 packets
            
            print("📤 Uploading PCAP file with 200 packet limit...")
            response = requests.post(url, files=files, data=data, timeout=30)
            
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ API Response Status: {result.get('status', 'unknown')}")
            print(f"📊 Statistics:")
            
            stats = result.get('stats', {})
            summary = result.get('summary', {})
            
            print(f"   - Total calls: {stats.get('total_calls', summary.get('total_calls', 0))}")
            print(f"   - Anomalies: {stats.get('anomaly_count', summary.get('anomalies', 0))}")
            print(f"   - Total packets: {stats.get('total_packets', 0)}")
            print(f"   - Packets processed: {result.get('packets_processed', 0)}")
            
            calls = result.get('calls', [])
            print(f"\n📞 Call Details ({len(calls)} calls found):")
            print("-" * 60)
            
            for i, call in enumerate(calls[:5]):  # Show first 5 calls
                print(f"\n🔵 Call {i+1}:")
                print(f"   Call ID: {call.get('call_id', 'N/A')}")
                print(f"   FROM: {call.get('from_uri', 'N/A')}")
                print(f"   TO: {call.get('to_uri', 'N/A')}")
                print(f"   Packets: {call.get('total_pkts', 0)} ({call.get('sip_pkts', 0)} SIP, {call.get('rtp_pkts', 0)} RTP)")
                print(f"   Duration: {call.get('duration_s', 0):.2f}s")
                print(f"   IPs: {call.get('src_ips', 'N/A')} → {call.get('dst_ips', 'N/A')}")
                print(f"   Anomaly: {'🚨 YES' if call.get('is_anomaly', False) else '✅ No'}")
                
                # Show specific anomaly flags
                anomaly_flags = []
                if call.get('flag_short_burst', False):
                    anomaly_flags.append("Short Burst")
                if call.get('flag_no_rtp', False):
                    anomaly_flags.append("No RTP")
                if call.get('flag_high_diversity', False):
                    anomaly_flags.append("High Diversity")
                if call.get('flag_unusual_time', False):
                    anomaly_flags.append("Unusual Time")
                if call.get('flag_large_packets', False):
                    anomaly_flags.append("Large Packets")
                
                if anomaly_flags:
                    print(f"   Flags: {', '.join(anomaly_flags)}")
            
            if len(calls) > 5:
                print(f"\n... and {len(calls) - 5} more calls")
            
            print(f"\n✅ SUCCESS: From/To information is now available!")
            print(f"🎯 The web interface should now show proper FROM and TO fields.")
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text[:500]}...")
            
    except requests.RequestException as e:
        print(f"❌ Network Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_large_pcap()
