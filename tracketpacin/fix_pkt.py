#!/usr/bin/env python3
"""Fix generated XML by removing corrupted physical workspace"""
import xml.etree.ElementTree as ET
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python fix_pkt.py <input.xml> [output.xml]")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.xml', '_fixed.xml')

print(f"Loading: {input_file}")
tree = ET.parse(input_file)
root = tree.getroot()

# Remove corrupted physical workspace
pw = root.find('PHYSICALWORKSPACE')
if pw is not None:
    root.remove(pw)
    print('✓ Removed corrupted PHYSICALWORKSPACE')
else:
    print('! No PHYSICALWORKSPACE found')

# Save fixed XML
tree.write(output_file, encoding='utf-8', xml_declaration=False)
print(f'✓ Saved fixed XML: {output_file}')
print(f'\nNow convert to .pkt with:')
print(f'  python ptexplorer.py -e {output_file} output.pkt')
