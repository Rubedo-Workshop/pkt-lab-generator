#!/usr/bin/env python3
"""Fix generated XML by replacing corrupted physical workspace with valid one from test.xml"""
import xml.etree.ElementTree as ET
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
test_xml = os.path.join(script_dir, 'test.xml')

if len(sys.argv) < 2:
    print("Usage: python fix_pkt_v2.py <input.xml> [output.xml]")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.xml', '_fixed.xml')

print(f"Loading: {input_file}")
tree = ET.parse(input_file)
root = tree.getroot()

# Load physical workspace from test.xml
print(f"Loading valid PHYSICALWORKSPACE from: {test_xml}")
test_tree = ET.parse(test_xml)
test_root = test_tree.getroot()
test_pw = test_root.find('PHYSICALWORKSPACE')

if test_pw is None:
    print("ERROR: test.xml has no PHYSICALWORKSPACE")
    sys.exit(1)

# Remove corrupted physical workspace
pw = root.find('PHYSICALWORKSPACE')
if pw is not None:
    root.remove(pw)
    print('✓ Removed corrupted PHYSICALWORKSPACE')

# Add valid physical workspace from test.xml
new_pw = ET.Element('PHYSICALWORKSPACE')
for child in test_pw:
    new_pw.append(ET.fromstring(ET.tostring(child)))
root.append(new_pw)
print('✓ Added valid PHYSICALWORKSPACE from test.xml')

# Save fixed XML
ET.indent(tree, space=' ')
tree.write(output_file, encoding='utf-8', xml_declaration=False)
print(f'✓ Saved fixed XML: {output_file}')
print(f'\nNow convert to .pkt with:')
print(f'  python ptexplorer.py -e {output_file} output.pkt')
