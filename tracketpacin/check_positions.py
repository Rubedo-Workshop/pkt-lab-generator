#!/usr/bin/env python3
"""Check device positions in generated XML"""
import xml.etree.ElementTree as ET
import sys

xml_file = sys.argv[1] if len(sys.argv) > 1 else 'ospf_lab.xml'

tree = ET.parse(xml_file)
root = tree.getroot()

network = root.find('NETWORK')
devices_elem = network.find('DEVICES')

print(f"\nChecking {xml_file}:")
print(f"Total devices: {len(list(devices_elem))}")
print("\nDevice positions (X, Y):")

for dev in devices_elem:
    name = dev.find('ENGINE/NAME')
    workspace = dev.find('WORKSPACE')
    if workspace is not None:
        logical = workspace.find('LOGICAL')
        if logical is not None:
            x = logical.find('X')
            y = logical.find('Y')
            print(f"  {name.text if name is not None else 'unknown'}: X={x.text if x is not None else '?'}, Y={y.text if y is not None else '?'}")

print("\nExpected visible range: X=100-800, Y=50-600")
print("Devices outside this range may not be visible!")
