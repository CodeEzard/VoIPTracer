#!/usr/bin/env python3
"""
Update existing PCAP files with more diverse data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generate_diverse_pcap import EnhancedPCAPGenerator

def update_existing_pcaps():
    """Update existing PCAP files with larger, more diverse data"""
    generator = EnhancedPCAPGenerator()
    
    # Update existing files with more comprehensive data
    updates = [
        ('sample_voip_traffic.pcap', 300, True, 'Mixed enterprise traffic with security events'),
        ('large_diverse_voip_traffic.pcap', 800, True, 'Large diverse dataset with international calls'),
        ('comprehensive_voip_traffic.pcap', 1200, True, 'Comprehensive dataset with all scenarios')
    ]
    
    for filename, num_calls, include_anomalies, description in updates:
        print(f"\nUpdating {filename}")
        print(f"Description: {description}")
        
        # Backup original file
        if os.path.exists(filename):
            backup_name = f"{filename}.backup"
            os.rename(filename, backup_name)
            print(f"Backed up original to {backup_name}")
        
        # Generate new diverse content
        generator.generate_large_diverse_pcap(filename, num_calls, include_anomalies)
        
        print(f"✓ Updated {filename} with {num_calls} calls")

if __name__ == "__main__":
    update_existing_pcaps()
