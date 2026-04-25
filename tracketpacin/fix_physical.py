#!/usr/bin/env python3
"""
Fix generated XML so Packet Tracer doesn't report corrupted physical workspace.

The root cause: each device's WORKSPACE/PHYSICAL UUID path must reference UUIDs
that actually exist in the global PHYSICALWORKSPACE hierarchy. Tracketpacin
generates random UUIDs that don't match. This script replaces both:
  1. The global PHYSICALWORKSPACE with the clean one from emptysavefile.xml
  2. Every device's WORKSPACE/PHYSICAL with the matching HOMERACK path
"""
import xml.etree.ElementTree as ET
import sys
import os
import uuid

script_dir = os.path.dirname(os.path.abspath(__file__))
empty_xml = os.path.join(script_dir, 'emptysavefile.xml')

if len(sys.argv) < 3:
    print("Usage: python fix_physical.py <input.xml> <output.xml>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# Load the clean workspace from emptysavefile
empty_tree = ET.parse(empty_xml)
empty_root = empty_tree.getroot()
clean_pw = empty_root.find('PHYSICALWORKSPACE')
if clean_pw is None:
    print("ERROR: emptysavefile.xml has no PHYSICALWORKSPACE")
    sys.exit(1)

# Extract the HOMERACK path (4 UUIDs: intercity, city, building, rack)
homerack_str = clean_pw.findtext('HOMERACK', '')
homerack_uuids = [u.strip() for u in homerack_str.split(',') if u.strip()]

# Parse the generated XML
tree = ET.parse(input_file)
root = tree.getroot()

# 1. Replace global PHYSICALWORKSPACE
pw = root.find('PHYSICALWORKSPACE')
if pw is not None:
    idx = list(root).index(pw)
    root.remove(pw)
    root.insert(idx, clean_pw)
else:
    root.append(clean_pw)

# 2. Fix every device's WORKSPACE/PHYSICAL to use a valid path
#    Format: {rack_uuid},{rack_uuid},{building_uuid},{city_uuid} + 2 device-specific UUIDs
#    (The working files show 6 UUIDs total: 4 path + 2 device-specific)
for device in root.findall('.//DEVICE'):
    ws = device.find('WORKSPACE')
    if ws is None:
        continue
    phys = ws.find('PHYSICAL')
    if phys is None:
        phys = ET.SubElement(ws, 'PHYSICAL')
    # Give each device its own unique slot UUID but share the rack path
    device_uuid = '{' + str(uuid.uuid4()) + '}'
    slot_uuid = '{' + str(uuid.uuid4()) + '}'
    phys.text = ','.join(homerack_uuids) + ',' + device_uuid + ',' + slot_uuid

tree.write(output_file, encoding='unicode', xml_declaration=False)
print(f"Fixed XML written to: {output_file}")
