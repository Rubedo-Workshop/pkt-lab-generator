#!/usr/bin/env python3
"""
Quick Start Examples - PKT Lab Generator
==========================================
Run these examples to generate sample .pkt files instantly.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pkt_lab_generator import quick_build_scenario, quick_build_custom, PKTLabGenerator, TopologyPlan, DeviceSpec, LinkSpec


def example_1_ospf_lab():
    """Example 1: Generate an OSPF lab from scenario template"""
    print("\n" + "="*70)
    print("Example 1: OSPF Validation Lab (from scenario)")
    print("="*70)
    
    result = quick_build_scenario(
        scenario_name='ospf_validation',
        output_path='ospf_lab.pkt',
        seed=42
    )
    
    print(f"\n✅ Generated OSPF lab successfully!")
    print(f"   Files created:")
    print(f"   - {result['xml']}")
    print(f"   - {result['pkt']}")


def example_2_custom_topology():
    """Example 2: Generate a custom topology lab"""
    print("\n" + "="*70)
    print("Example 2: Custom Topology Lab (from specification)")
    print("="*70)
    
    devices = [
        {"name": "R1", "device_type": "router"},
        {"name": "SW1", "device_type": "switch"},
        {"name": "PC1", "device_type": "pc"},
        {"name": "PC2", "device_type": "pc"},
    ]
    
    links = [
        {"dev1": "R1", "port1": "Gig0/0", "dev2": "SW1", "port2": "Gig0/1"},
        {"dev1": "SW1", "port1": "Fa0/1", "dev2": "PC1", "port2": "FastEthernet0"},
        {"dev1": "SW1", "port1": "Fa0/2", "dev2": "PC2", "port2": "FastEthernet0"},
    ]
    
    result = quick_build_custom(
        devices=devices,
        links=links,
        output_path='simple_lab.pkt',
        routing_protocol='ospf',
        dhcp_enabled=True,
        seed=123
    )
    
    print(f"\n✅ Generated custom lab successfully!")
    print(f"   Files created:")
    print(f"   - {result['xml']}")
    print(f"   - {result['pkt']}")


def example_3_vlan_lab():
    """Example 3: Generate a VLAN lab"""
    print("\n" + "="*70)
    print("Example 3: VLAN Lab (from scenario)")
    print("="*70)
    
    result = quick_build_scenario(
        scenario_name='vlan_inter',
        output_path='vlan_lab.pkt',
        seed=99
    )
    
    print(f"\n✅ Generated VLAN lab successfully!")
    print(f"   Files created:")
    print(f"   - {result['xml']}")
    print(f"   - {result['pkt']}")


def example_4_programmatic():
    """Example 4: Programmatic API usage"""
    print("\n" + "="*70)
    print("Example 4: Programmatic API Usage")
    print("="*70)
    
    # Create plan
    plan = TopologyPlan(
        devices=[
            DeviceSpec(name="HQ-RTR", device_type="router"),
            DeviceSpec(name="HQ-SW", device_type="switch"),
            DeviceSpec(name="Branch-RTR", device_type="router"),
            DeviceSpec(name="HQ-PC1", device_type="pc"),
        ],
        links=[
            LinkSpec(dev1="HQ-RTR", port1="Gig0/0", dev2="HQ-SW", port2="Gig0/1"),
            LinkSpec(dev1="HQ-RTR", port1="Serial0/0/0", dev2="Branch-RTR", port2="Serial0/0/0", cable_type="eSerial"),
            LinkSpec(dev1="HQ-SW", port1="Fa0/1", dev2="HQ-PC1", port2="FastEthernet0"),
        ],
        routing_protocol='ospf',
        metadata={'purpose': 'WAN simulation'}
    )
    
    # Build lab
    generator = PKTLabGenerator(seed=42)
    generator.from_spec(plan)
    generator.enhance_with_mcp_rules()
    generator.generate_configs()
    generator.export_xml('wan_lab.xml')
    generator.export_pkt('wan_lab.xml', 'wan_lab.pkt')
    
    print(f"\n✅ Generated WAN lab successfully!")
    print(f"   Files created:")
    print(f"   - wan_lab.xml")
    print(f"   - wan_lab.pkt")


if __name__ == '__main__':
    print("\n" + "="*70)
    print("PKT Lab Generator - Quick Start Examples")
    print("="*70)
    
    # Run all examples
    try:
        example_1_ospf_lab()
    except Exception as e:
        print(f"\n❌ Example 1 failed: {e}")
    
    try:
        example_2_custom_topology()
    except Exception as e:
        print(f"\n❌ Example 2 failed: {e}")
    
    try:
        example_3_vlan_lab()
    except Exception as e:
        print(f"\n❌ Example 3 failed: {e}")
    
    try:
        example_4_programmatic()
    except Exception as e:
        print(f"\n❌ Example 4 failed: {e}")
    
    print("\n" + "="*70)
    print("All examples completed!")
    print("="*70 + "\n")
