# VoIP PCAP Generation Guide

## 🎯 Generated Sample PCAP File
Your VoIP Tracer now has a sample PCAP file: `sample_voip_traffic.pcap`

**Contains:**
- 5 VoIP calls with different scenarios
- SIP signaling packets (INVITE, 200 OK)
- Bidirectional RTP audio streams  
- Suspicious calling patterns
- 8,134 total packets (625 KB)

## 🛠️ Alternative Methods to Generate VoIP PCAPs

### Method 1: Using Wireshark/TShark (Recommended)
```bash
# Install Wireshark first, then use tshark
tshark -i eth0 -f "port 5060 or portrange 8000-65000" -w voip_capture.pcap

# Or capture existing network traffic
tshark -r existing_network.pcap -Y "sip or rtp" -w voip_only.pcap
```

### Method 2: Using SIPp (Professional Tool)
```bash
# Install SIPp
sudo apt-get install sipp  # Linux
brew install sipp          # macOS

# Generate SIP traffic
sipp -sn uac 192.168.1.100:5060 -l 10 -m 100
```

### Method 3: Online Sample PCAP Files
Download pre-made VoIP PCAP files from:

1. **Wireshark Sample Captures:**
   - https://wiki.wireshark.org/SampleCaptures
   - Look for: SIP, RTP, VoIP samples

2. **Malware Traffic Analysis:**
   - https://malware-traffic-analysis.net/
   - Contains real-world network captures

3. **PacketLife.net:**
   - http://packetlife.net/captures/
   - Various protocol samples including VoIP

### Method 4: Asterisk/FreePBX Test Calls
If you have access to an Asterisk PBX:
```bash
# Make test calls and capture
tcpdump -i any -s 65535 -w voip_test.pcap port 5060 or portrange 10000-20000
```

### Method 5: Custom Python Generator (What We Just Used)
```python
# Run our generator with different parameters
python generate_voip_pcap.py
```

## 📋 PCAP File Requirements for VoIP Tracer

Your PCAP should contain:
- **SIP packets** (port 5060) for call signaling
- **RTP packets** (high ports) for audio streams  
- **RTCP packets** for quality reporting
- **Proper IP addresses** and port ranges
- **Call-ID headers** in SIP messages

## 🧪 Testing Your PCAP File

Use our debug tool:
```bash
python pcap_debug.py your_file.pcap
```

This will show:
- Total packets and protocols
- VoIP packet detection results
- Common ports and traffic patterns
- Extraction success/failure

## 🎯 Upload to VoIP Tracer

1. Start the backend: `python -m uvicorn src.api:app --host 0.0.0.0 --port 8002`
2. Start the frontend: `cd frontend && npm run dev`
3. Go to: http://localhost:5173
4. Upload your PCAP file
5. View analysis results

## 🚨 Common Issues

**"No VoIP packets found":**
- Check if PCAP contains SIP/RTP traffic
- Verify port ranges (5060 for SIP, 8000+ for RTP)
- Use tcpdump with proper filters
- Try our debug tool first

**Event loop errors:**
- We've fixed the asyncio conflicts
- Backend now handles pyshark properly
- Use threading for packet processing

## 💡 Pro Tips

1. **Capture real traffic** during actual VoIP calls for best results
2. **Use proper filters** when capturing (sip or rtp)
3. **Include both signaling and media** for complete analysis
4. **Test with our sample file first** to verify the system works
5. **Check file permissions** and size limits (100MB max)
