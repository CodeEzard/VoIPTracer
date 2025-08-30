#!/usr/bin/env python3
"""
Generate smaller PCAP files optimized for web upload
Maximum 5MB per file with high-quality diverse data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generate_diverse_pcap import EnhancedPCAPGenerator

def create_upload_optimized_pcaps():
    """Create smaller PCAP files optimized for web upload (under 5MB each)"""
    generator = EnhancedPCAPGenerator()
    
    # Create upload-optimized files (smaller but still diverse)
    upload_files = [
        ('demo_small.pcap', 50, True, 'Small demo with anomalies - perfect for testing uploads'),
        ('enterprise_sample.pcap', 100, True, 'Enterprise sample with security events'),
        ('international_sample.pcap', 80, False, 'International calls sample'),
        ('suspicious_small.pcap', 30, True, 'Focused suspicious activity sample'),
        ('normal_calls.pcap', 120, False, 'Normal call patterns only'),
    ]
    
    print("Creating upload-optimized PCAP files (under 5MB each)...")
    print("=" * 60)
    
    for filename, num_calls, include_anomalies, description in upload_files:
        print(f"\nGenerating: {filename}")
        print(f"Description: {description}")
        print(f"Calls: {num_calls}, Anomalies: {include_anomalies}")
        
        generator.generate_large_diverse_pcap(filename, num_calls, include_anomalies)
        
        # Check file size
        file_size = os.path.getsize(filename)
        file_size_mb = file_size / (1024 * 1024)
        
        if file_size_mb > 5:
            print(f"⚠️  Warning: {filename} is {file_size_mb:.2f}MB (over 5MB limit)")
        else:
            print(f"✓ {filename} created: {file_size_mb:.2f}MB (upload-friendly)")
    
    print("\n" + "=" * 60)
    print("Upload-optimized files created!")
    print("These files are designed for web upload testing and demos.")

if __name__ == "__main__":
    create_upload_optimized_pcaps()
