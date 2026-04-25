#!/usr/bin/env python3
"""Compare device structure between test.xml and generated XML"""
import xml.etree.ElementTree as ET

# Load both files
test_tree = ET.parse('test.xml')
test_root = test_tree.getroot()

lab_tree = ET.parse('ospf_lab.xml')
lab_root = lab_tree.getroot()

# Get first device from each
test_devices = test_root.find('NETWORK').find('DEVICES').findall('DEVICE')
lab_devices = lab_root.find('NETWORK').find('DEVICES').findall('DEVICE')

print("=== test.xml first device structure ===")
dev1 = test_devices[0]
print(f"Device type: {dev1.findtext('ENGINE/TYPE')}")
print(f"Top-level tags: {[child.tag for child in dev1]}")

print("\n=== ospf_lab.xml first device structure ===")
dev2 = lab_devices[0]
print(f"Device type: {dev2.findtext('ENGINE/TYPE')}")
print(f"Top-level tags: {[child.tag for child in dev2]}")

# Check for LOGICAL element
print("\n=== Checking LOGICAL workspace ===")
test_logical = dev1.find('WORKSPACE/LOGICAL')
lab_logical = dev2.find('WORKSPACE/LOGICAL')

print(f"test.xml LOGICAL tags: {[child.tag for child in test_logical] if test_logical is not None else 'MISSING'}")
print(f"ospf_lab.xml LOGICAL tags: {[child.tag for child in lab_logical] if lab_logical is not None else 'MISSING'}")

# Check for missing elements
if test_logical is not None and lab_logical is not None:
    test_tags = set(child.tag for child in test_logical)
    lab_tags = set(child.tag for child in lab_logical)
    
    missing = test_tags - lab_tags
    extra = lab_tags - test_tags
    
    if missing:
        print(f"\n⚠️  ospf_lab.xml MISSING tags: {missing}")
    if extra:
        print(f"\n+ ospf_lab.xml has extra tags: {extra}")
    if not missing and not extra:
        print("\n✅ LOGICAL structure matches!")
