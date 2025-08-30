"""Capture and extract VoIP metadata from pcap files or live traffic."""

import pyshark
import asyncio
import threading
import sys
from typing import Dict, List, Generator, Optional


def read_pcap(path: str, limit: Optional[int] = None) -> Generator[Dict, None, None]:
    """Read pcap file and yield VoIP metadata dicts.
    
    Args:
        path: Path to pcap file
        limit: Max packets to process (None = all)
    
    Yields:
        Dict with SIP/RTP/TLS metadata
    """
    def _run_in_thread():
        """Run pyshark in a separate thread to avoid event loop conflicts"""
        packets = []
        try:
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            print(f"Reading PCAP file: {path}")
            
            # First try: Use broad filter to catch VoIP traffic
            display_filter = "sip or rtp or rtcp or h323 or megaco or mgcp or sccp or udp.port==5060 or tcp.port==5060 or udp.port==1719 or tcp.port==1719"
            print(f"Applied filter: {display_filter}")
            
            try:
                cap = pyshark.FileCapture(path, display_filter=display_filter)
                count = 0
                
                for pkt in cap:
                    if limit and count >= limit:
                        break
                    meta = extract_meta(pkt)
                    if meta:
                        packets.append(meta)
                        count += 1
                        if count % 100 == 0:  # Progress indicator
                            print(f"Processed {count} VoIP packets...")
                
                cap.close()
                print(f"Filtered extraction complete: {len(packets)} VoIP packets found")
                
            except Exception as e:
                print(f"Filtered capture failed: {e}")
            
            # If we didn't find VoIP packets with filter, try without filter and analyze
            if len(packets) == 0:
                print("No VoIP packets found with filter. Trying without filter for analysis...")
                try:
                    cap = pyshark.FileCapture(path)
                    count = 0
                    protocols_seen = set()
                    port_analysis = {}
                    
                    for pkt in cap:
                        if limit and count >= 1000:  # Limit analysis to first 1000 packets
                            break
                        
                        # Collect protocol statistics
                        if hasattr(pkt, 'highest_layer'):
                            protocols_seen.add(pkt.highest_layer)
                        
                        # Collect port statistics
                        if hasattr(pkt, 'tcp'):
                            src_port = int(pkt.tcp.srcport)
                            dst_port = int(pkt.tcp.dstport)
                            port_analysis[f"TCP {src_port}"] = port_analysis.get(f"TCP {src_port}", 0) + 1
                            port_analysis[f"TCP {dst_port}"] = port_analysis.get(f"TCP {dst_port}", 0) + 1
                        elif hasattr(pkt, 'udp'):
                            src_port = int(pkt.udp.srcport)
                            dst_port = int(pkt.udp.dstport)
                            port_analysis[f"UDP {src_port}"] = port_analysis.get(f"UDP {src_port}", 0) + 1
                            port_analysis[f"UDP {dst_port}"] = port_analysis.get(f"UDP {dst_port}", 0) + 1
                        
                        # Try to extract meta even without VoIP filter
                        meta = extract_meta(pkt)
                        if meta and meta['proto']:
                            packets.append(meta)
                        
                        count += 1
                    
                    cap.close()
                    
                    print(f"Analysis complete: {count} total packets analyzed")
                    print(f"Protocols found: {', '.join(sorted(protocols_seen))}")
                    print("Top ports:")
                    for port, count in sorted(port_analysis.items(), key=lambda x: x[1], reverse=True)[:10]:
                        print(f"  {port}: {count} packets")
                    print(f"VoIP packets extracted: {len(packets)}")
                    
                except Exception as e2:
                    print(f"Unfiltered analysis also failed: {e2}")
            
            loop.close()
            
        except Exception as e:
            print(f"Error processing pcap: {e}")
        
        return packets
    
    try:
        # Check if we're in an async context
        try:
            loop = asyncio.get_running_loop()
            # We're in an async context, run in thread
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(_run_in_thread)
                packets = future.result(timeout=120)  # 2 minute timeout
        except RuntimeError:
            # No running loop, safe to run directly
            packets = _run_in_thread()
        
        for packet in packets:
            yield packet
            
    except Exception as e:
        print(f"Error opening pcap file {path}: {e}")
        return


def read_live(iface: str = "eth0", limit: Optional[int] = None) -> Generator[Dict, None, None]:
    """Live capture VoIP metadata.
    
    Args:
        iface: Network interface
        limit: Max packets to process
    
    Yields:
        Dict with VoIP metadata
    """
    cap = pyshark.LiveCapture(interface=iface, display_filter="sip or rtp or tls or dtls")
    
    count = 0
    for pkt in cap.sniff_continuously():
        if limit and count >= limit:
            break
            
        meta = extract_meta(pkt)
        if meta:
            yield meta
            count += 1


def extract_meta(pkt) -> Optional[Dict]:
    """Extract metadata from a single packet."""
    try:
        meta = {
            'ts': float(pkt.sniff_timestamp) if hasattr(pkt, 'sniff_timestamp') else 0.0,
            'src_ip': pkt.ip.src if hasattr(pkt, 'ip') else '',
            'dst_ip': pkt.ip.dst if hasattr(pkt, 'ip') else '',
            'src_port': 0,
            'dst_port': 0,
            'proto': '',
            'call_id': '',
            'from_uri': '',
            'to_uri': '',
            'ssrc': 0,
            'pkt_len': int(pkt.length),
            'tls_ver': '',
            'ja3': ''
        }
        
        # Extract port information
        if hasattr(pkt, 'tcp'):
            meta['src_port'] = int(pkt.tcp.srcport)
            meta['dst_port'] = int(pkt.tcp.dstport)
        elif hasattr(pkt, 'udp'):
            meta['src_port'] = int(pkt.udp.srcport)
            meta['dst_port'] = int(pkt.udp.dstport)
        
        # Check for VoIP protocols in order of priority
        
        # SIP metadata (highest priority)
        if hasattr(pkt, 'sip'):
            meta['proto'] = 'SIP'
            try:
                if hasattr(pkt.sip, 'call_id'):
                    meta['call_id'] = str(pkt.sip.call_id)
                if hasattr(pkt.sip, 'from'):
                    meta['from_uri'] = str(getattr(pkt.sip, 'from'))
                if hasattr(pkt.sip, 'to'):
                    meta['to_uri'] = str(pkt.sip.to)
            except Exception as e:
                print(f"Error extracting SIP metadata: {e}")
        
        # RTP metadata
        elif hasattr(pkt, 'rtp'):
            meta['proto'] = 'RTP'
            try:
                if hasattr(pkt.rtp, 'ssrc'):
                    meta['ssrc'] = int(pkt.rtp.ssrc, 16)
            except Exception as e:
                print(f"Error extracting RTP metadata: {e}")
        
        # RTCP metadata
        elif hasattr(pkt, 'rtcp'):
            meta['proto'] = 'RTCP'
            try:
                if hasattr(pkt.rtcp, 'ssrc'):
                    meta['ssrc'] = int(pkt.rtcp.ssrc, 16)
            except Exception as e:
                print(f"Error extracting RTCP metadata: {e}")
        
        # Check for VoIP ports even if protocol not detected
        elif meta['src_port'] == 5060 or meta['dst_port'] == 5060:
            meta['proto'] = 'SIP'  # Likely SIP on standard port
        elif meta['src_port'] == 1719 or meta['dst_port'] == 1719:
            meta['proto'] = 'H323'  # H.323 RAS
        elif 8000 <= meta['src_port'] <= 65535 and 8000 <= meta['dst_port'] <= 65535:
            # Could be RTP on high ports
            if hasattr(pkt, 'udp') and pkt.udp:
                meta['proto'] = 'RTP'  # Assume RTP for UDP on high ports
        
        # TLS/DTLS metadata (for secure VoIP)
        elif hasattr(pkt, 'tls'):
            meta['proto'] = 'TLS'
            try:
                if hasattr(pkt.tls, 'handshake_version'):
                    meta['tls_ver'] = str(pkt.tls.handshake_version)
                meta['ja3'] = 'tls_detected'  # Placeholder
            except Exception as e:
                print(f"Error extracting TLS metadata: {e}")
        
        elif hasattr(pkt, 'dtls'):
            meta['proto'] = 'DTLS'
            meta['ja3'] = 'dtls_detected'  # Placeholder
        
        # H.323 protocols
        elif hasattr(pkt, 'h225') or hasattr(pkt, 'h245'):
            meta['proto'] = 'H323'
        
        # MGCP/Megaco
        elif hasattr(pkt, 'mgcp'):
            meta['proto'] = 'MGCP'
        elif hasattr(pkt, 'megaco'):
            meta['proto'] = 'MEGACO'
        
        # SCCP (Skinny)
        elif hasattr(pkt, 'sccp') or hasattr(pkt, 'skinny'):
            meta['proto'] = 'SCCP'
        
        # More aggressive port-based detection for common VoIP ranges
        elif hasattr(pkt, 'udp'):
            src_port = meta['src_port']
            dst_port = meta['dst_port']
            
            # Common VoIP ports and ranges
            voip_ports = [5060, 5061, 1719, 1720, 2427, 2727, 5004, 5005]
            rtp_ranges = [(16384, 32767), (49152, 65535), (10000, 20000), (6000, 6999)]
            
            if src_port in voip_ports or dst_port in voip_ports:
                meta['proto'] = 'SIP' if (src_port == 5060 or dst_port == 5060) else 'VoIP'
            else:
                # Check if ports fall in common RTP ranges
                for start, end in rtp_ranges:
                    if (start <= src_port <= end) or (start <= dst_port <= end):
                        meta['proto'] = 'RTP'
                        break
        
        # TCP-based VoIP protocols
        elif hasattr(pkt, 'tcp'):
            src_port = meta['src_port']
            dst_port = meta['dst_port']
            
            # SIP over TCP, H.323, etc.
            if src_port in [5060, 5061, 1720] or dst_port in [5060, 5061, 1720]:
                meta['proto'] = 'SIP' if (src_port in [5060, 5061] or dst_port in [5060, 5061]) else 'H323'
        
        # Look for packet content patterns that might indicate VoIP
        elif hasattr(pkt, 'udp'):
            try:
                # Check if this looks like RTP (basic heuristic)
                # RTP packets typically have:
                # - UDP transport
                # - Payload size that makes sense (20-200 bytes typically)
                # - Regular intervals
                payload_size = meta['pkt_len'] - 42  # Subtract Ethernet + IP + UDP headers
                if 20 <= payload_size <= 300 and hasattr(pkt, 'udp'):
                    # This could be RTP, mark it for potential VoIP traffic
                    meta['proto'] = 'UDP_CANDIDATE'
            except:
                pass
        
        # Return packet if we detected any VoIP protocol or candidate
        return meta if meta['proto'] else None
        
    except Exception as e:
        print(f"Error extracting packet metadata: {e}")
        return None
