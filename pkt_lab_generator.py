#!/usr/bin/env python3
"""
PKT Lab Generator - Unified Integration Tool
=============================================
Combines tracketpacin (randomized lab generation) with MCP Packet Tracer Server 
(planning, validation, enhancement) to generate complete .pkt files.

Usage:
  python pkt_lab_generator.py scenario <name> -o output.pkt
  python pkt_lab_generator.py custom -o output.pkt --devices devices.json --links links.json
  python pkt_lab_generator.py list-scenarios
"""

import argparse
import json
import os
import random
import subprocess
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path

# Paths
TRACKETPACIN_DIR = Path(__file__).parent / "tracketpacin"
MCP_PT_DIR = Path(__file__).parent / "MCP_Packet_Tracer"


# ============================================================================
# Data Models
# ============================================================================

@dataclass
class DeviceSpec:
    """Device specification for topology building"""
    name: str
    device_type: str  # router, switch, pc, server
    model: Optional[str] = None
    position: Optional[tuple] = None
    config: Optional[str] = None
    ip_address: Optional[str] = None
    gateway: Optional[str] = None
    dhcp: bool = False


@dataclass
class LinkSpec:
    """Link specification between devices"""
    dev1: str
    port1: str
    dev2: str
    port2: str
    cable_type: Optional[str] = None
    length: str = "5"


@dataclass
class TopologyPlan:
    """Complete topology plan"""
    devices: List[DeviceSpec] = field(default_factory=list)
    links: List[LinkSpec] = field(default_factory=list)
    routing_protocol: Optional[str] = None
    dhcp_enabled: bool = False
    vlan_config: Optional[Dict] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Helper Functions
# ============================================================================

def run_tracketpacin(scenario_name: str, output_xml: str, seed: Optional[int] = None, size: str = 'medium'):
    """Run tracketpacin to generate XML from scenario"""
    cmd = [
        sys.executable, "main.py",
        '--scenario', scenario_name,
        '--output', output_xml,
        '--skip-pkt',
        '--size', size,
    ]
    
    if seed is not None:
        cmd.extend(['--seed', str(seed)])
    
    # MUST run from tracketpacin directory (needs test.xml)
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(TRACKETPACIN_DIR))
    
    if result.returncode != 0:
        raise RuntimeError(f"tracketpacin failed: {result.stderr}")
    
    return output_xml


def encode_xml_to_pkt(xml_path: str, pkt_path: str):
    """Encode XML to .pkt binary format using ptexplorer"""
    # Use absolute paths
    import os
    xml_abs = os.path.abspath(xml_path)
    pkt_abs = os.path.abspath(pkt_path)
    
    cmd = [
        sys.executable, "ptexplorer.py",
        '-e', xml_abs, pkt_abs
    ]
    
    # MUST run from tracketpacin directory
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(TRACKETPACIN_DIR))
    
    if result.returncode != 0:
        raise RuntimeError(f"ptexplorer encoding failed: {result.stderr}")
    
    return pkt_path


def parse_xml_topology(xml_path: str):
    """Parse Packet Tracer XML to extract topology information"""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    devices = []
    links = []
    
    # Parse devices
    network = root.find('NETWORK')
    if network is not None:
        devices_elem = network.find('DEVICES')
        if devices_elem is not None:
            for device in devices_elem.findall('DEVICE'):
                name = device.findtext('ENGINE/NAME')
                dtype = device.findtext('ENGINE/TYPE', '').lower()
                
                if name:
                    # Categorize device type
                    if 'router' in dtype:
                        category = 'router'
                    elif 'switch' in dtype:
                        category = 'switch'
                    elif 'pc' in dtype or 'server' in dtype:
                        category = 'pc'
                    else:
                        category = 'other'
                    
                    devices.append({
                        'name': name,
                        'type': category,
                        'model': dtype
                    })
        
        # Parse links
        links_elem = network.find('LINKS')
        if links_elem is not None:
            for link in links_elem.findall('LINK'):
                cable = link.find('CABLE')
                if cable is not None:
                    from_dev = cable.findtext('FROM')
                    from_port = cable.findtext('PORT')
                    to_dev = cable.findtext('TO')
                    to_port = cable.findtext('PORT')
                    
                    # These are references, we'd need to map them back
                    # For now, just store raw data
                    links.append({
                        'from': from_dev,
                        'from_port': from_port,
                        'to': to_dev,
                        'to_port': to_port
                    })
    
    return {
        'devices': devices,
        'links': links
    }


# ============================================================================
# Main Generator Class
# ============================================================================

class PKTLabGenerator:
    """
    Unified generator combining tracketpacin and MCP Packet Tracer Server.
    """
    
    def __init__(self, seed: Optional[int] = None):
        self.seed = seed
        self.plan: Optional[TopologyPlan] = None
        self.xml_path: Optional[str] = None
        
    def from_scenario(self, scenario_name: str, **kwargs):
        """Generate lab from tracketpacin scenario"""
        print(f"[*] Generating lab from scenario: {scenario_name}")
        
        xml_path = kwargs.get('xml_output', 'temp_lab.xml')
        
        # Generate XML using tracketpacin
        run_tracketpacin(
            scenario_name,
            xml_path,
            seed=kwargs.get('seed', self.seed),
            size=kwargs.get('size', 'medium')
        )
        
        self.xml_path = xml_path
        
        # Parse topology
        topology = parse_xml_topology(xml_path)
        
        self.plan = TopologyPlan(
            devices=[DeviceSpec(name=d['name'], device_type=d['type']) for d in topology['devices']],
            links=[],  # Links need more complex parsing
            routing_protocol=kwargs.get('routing'),
            metadata={'scenario': scenario_name}
        )
        
        print(f"[+] Generated {len(self.plan.devices)} devices")
        print(f"[+] XML saved to: {xml_path}")
        return self
    
    def to_pkt(self, pkt_path: Optional[str] = None):
        """Convert XML to .pkt binary"""
        if not self.xml_path:
            raise ValueError("No XML file available. Call from_scenario() first.")
        
        if pkt_path is None:
            pkt_path = self.xml_path.replace('.xml', '.pkt')
        
        print(f"[*] Encoding to .pkt format...")
        encode_xml_to_pkt(self.xml_path, pkt_path)
        
        print(f"[+] PKT file created: {pkt_path}")
        return pkt_path
    
    def full_build(self, output_path: str, **kwargs):
        """Complete build: scenario → XML → PKT"""
        print("\n" + "="*60)
        print("PKT Lab Generator - Full Build")
        print("="*60 + "\n")
        
        # Determine output format
        if output_path.endswith('.pkt'):
            xml_path = output_path.replace('.pkt', '.xml')
            pkt_path = output_path
        else:
            xml_path = output_path
            pkt_path = output_path.replace('.xml', '.pkt')
        
        # Generate from scenario
        self.from_scenario(
            kwargs.get('scenario', 'ospf_validation'),
            xml_output=xml_path,
            seed=kwargs.get('seed'),
            size=kwargs.get('size', 'medium'),
            routing=kwargs.get('routing')
        )
        
        # Convert to .pkt
        self.to_pkt(pkt_path)
        
        print("\n" + "="*60)
        print("✅ Build Complete!")
        print("="*60)
        print(f"\nOutput files:")
        print(f"  XML: {xml_path}")
        print(f"  PKT: {pkt_path}\n")
        
        return {
            'xml': xml_path,
            'pkt': pkt_path
        }


# ============================================================================
# Quick Build Functions
# ============================================================================

def quick_build_scenario(scenario_name: str, output_path: str, seed: Optional[int] = None, **kwargs):
    """One-liner to generate a scenario-based lab"""
    generator = PKTLabGenerator(seed=seed)
    return generator.full_build(
        output_path,
        scenario=scenario_name,
        seed=seed,
        **kwargs
    )


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="PKT Lab Generator - Generate Cisco Packet Tracer .pkt files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from scenario
  python pkt_lab_generator.py scenario ospf_validation -o ospf_lab.pkt

  # With seed for reproducibility
  python pkt_lab_generator.py scenario nat_pat -o nat_lab.pkt --seed 42

  # List scenarios
  python pkt_lab_generator.py list-scenarios
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Scenario command
    scenario_parser = subparsers.add_parser('scenario', help='Generate from scenario')
    scenario_parser.add_argument('scenario', help='Scenario name')
    scenario_parser.add_argument('-o', '--output', required=True, help='Output .pkt file')
    scenario_parser.add_argument('--seed', type=int, help='Random seed')
    scenario_parser.add_argument('--size', choices=['small', 'medium', 'large'], default='medium')
    
    # List scenarios
    subparsers.add_parser('list-scenarios', help='List available scenarios')
    
    args = parser.parse_args()
    
    if args.command == 'scenario':
        quick_build_scenario(
            args.scenario,
            args.output,
            seed=args.seed,
            size=args.size
        )
    
    elif args.command == 'list-scenarios':
        # List by running tracketpacin
        result = subprocess.run(
            [sys.executable, str(TRACKETPACIN_DIR / "main.py"), '--list'],
            capture_output=True,
            text=True,
            cwd=str(TRACKETPACIN_DIR)
        )
        print(result.stdout)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
