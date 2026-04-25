#!/usr/bin/env python3
"""
Lab generator: takes a decoded real PT XML, injects new configs, re-encodes to PKT.
Usage: python lab_gen.py <lab_name>
"""
import xml.etree.ElementTree as ET
import subprocess
import sys
import os
import textwrap

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRACER_DIR = os.path.join(SCRIPT_DIR, 'tracketpacin')

BASE_XMLS = {
    'routing': os.path.join(TRACER_DIR, 'static_mid.xml'),   # 6 routers, 4 PCs
    'acl':     os.path.join(TRACER_DIR, 'acl1.xml'),          # 2 routers, 2 switches, 6 PCs
    'eigrp':   os.path.join(TRACER_DIR, 'eigrp_template.xml'),# 4 routers, 6 switches, 9 PCs
}

# ── config helpers ────────────────────────────────────────────────────────────

def set_config(device_elem, config_text):
    """Write IOS config into RUNNINGCONFIG (replaces existing)."""
    engine = device_elem.find('ENGINE')
    for tag in ('RUNNINGCONFIG', 'STARTUPCONFIG'):
        section = engine.find(tag)
        if section is None:
            section = ET.SubElement(engine, tag)
        section.clear()
        if config_text:
            for line in config_text.strip('\n').splitlines():
                ET.SubElement(section, 'LINE').text = line

def clear_config(device_elem):
    set_config(device_elem, '')

def get_device(tree, name):
    for d in tree.findall('.//DEVICE'):
        if d.findtext('ENGINE/NAME') == name:
            return d
    return None

# ── labs ──────────────────────────────────────────────────────────────────────

LABS = {}

def lab(name, base, description):
    def decorator(fn):
        LABS[name] = {'base': base, 'fn': fn, 'description': description}
        return fn
    return decorator


@lab('ospf_basic', 'routing', 'OSPF single-area lab: 3 routers, configure OSPF process 1 in area 0')
def ospf_basic(tree):
    # Topology from static_mid.xml: RouterA, RouterD, RouterB, RouterC, Main_A, Main_B
    # We'll use RouterA, RouterB, RouterC in a triangle with PCs

    devices = {d.findtext('ENGINE/NAME'): d for d in tree.findall('.//DEVICE')}

    # RouterA: 192.168.1.0/30 to RouterB, 10.0.0.0/30 to RouterC, LAN 172.16.1.0/24
    set_config(devices['RouterA'], """\
!
hostname RouterA
!
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/1
 ip address 10.0.0.1 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/2
 ip address 172.16.1.1 255.255.255.0
 no shutdown
!
router ospf 1
 network 192.168.1.0 0.0.0.3 area 0
 network 10.0.0.0 0.0.0.3 area 0
 network 172.16.1.0 0.0.0.255 area 0
!
end""")

    set_config(devices['RouterB'], """\
!
hostname RouterB
!
interface GigabitEthernet0/0
 ip address 192.168.1.2 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/1
 ip address 192.168.2.1 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/2
 ip address 172.16.2.1 255.255.255.0
 no shutdown
!
router ospf 1
 network 192.168.1.0 0.0.0.3 area 0
 network 192.168.2.0 0.0.0.3 area 0
 network 172.16.2.0 0.0.0.255 area 0
!
end""")

    set_config(devices['RouterC'], """\
!
hostname RouterC
!
interface GigabitEthernet0/0
 ip address 10.0.0.2 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/1
 ip address 192.168.2.2 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/2
 ip address 172.16.3.1 255.255.255.0
 no shutdown
!
router ospf 1
 network 10.0.0.0 0.0.0.3 area 0
 network 192.168.2.0 0.0.0.3 area 0
 network 172.16.3.0 0.0.0.255 area 0
!
end""")

    # Clear unused routers
    for name in ('RouterD', 'Main_A', 'Main_B'):
        if name in devices:
            clear_config(devices[name])

    objectives = textwrap.dedent("""\
    # OSPF Basic Lab

    ## Topology
    - RouterA ↔ RouterB  Link: 192.168.1.0/30
    - RouterA ↔ RouterC  Link: 10.0.0.0/30
    - RouterB ↔ RouterC  Link: 192.168.2.0/30
    - RouterA LAN: 172.16.1.0/24
    - RouterB LAN: 172.16.2.0/24
    - RouterC LAN: 172.16.3.0/24

    ## Pre-configured (already done for you)
    - All router IPs and interfaces are configured and up
    - OSPF process 1 is running on all routers in area 0

    ## Your Tasks
    1. Verify OSPF adjacencies are up: `show ip ospf neighbor`
    2. Verify full routing tables: `show ip route ospf`
    3. Test end-to-end ping from 172.16.1.0/24 to 172.16.3.0/24
    4. On RouterA, change the OSPF cost of Gig0/0 to 100. Verify the routing table changes.
    5. Configure OSPF authentication (MD5) on the RouterA–RouterB link.
       Password: ccna123
    6. Add a loopback on RouterA (10.10.10.1/32) and advertise it in OSPF.

    ## Verification
    - `show ip ospf neighbor` — should show FULL state on all adjacencies
    - `show ip route` — should have O routes to all remote networks
    - `ping` between PC hosts on different LANs should succeed
    """)
    return objectives


@lab('static_routing', 'routing', 'Static routing lab: configure routes between 4 routers')
def static_routing(tree):
    devices = {d.findtext('ENGINE/NAME'): d for d in tree.findall('.//DEVICE')}

    set_config(devices['RouterA'], """\
!
hostname RouterA
!
interface GigabitEthernet0/0
 ip address 10.0.12.1 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/1
 ip address 172.16.1.1 255.255.255.0
 no shutdown
!
end""")

    set_config(devices['RouterB'], """\
!
hostname RouterB
!
interface GigabitEthernet0/0
 ip address 10.0.12.2 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/1
 ip address 10.0.23.1 255.255.255.252
 no shutdown
!
end""")

    set_config(devices['RouterC'], """\
!
hostname RouterC
!
interface GigabitEthernet0/0
 ip address 10.0.23.2 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/1
 ip address 10.0.34.1 255.255.255.252
 no shutdown
!
end""")

    set_config(devices['RouterD'], """\
!
hostname RouterD
!
interface GigabitEthernet0/0
 ip address 10.0.34.2 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/1
 ip address 192.168.4.1 255.255.255.0
 no shutdown
!
end""")

    for name in ('Main_A', 'Main_B'):
        if name in devices:
            clear_config(devices[name])

    objectives = textwrap.dedent("""\
    # Static Routing Lab

    ## Topology (linear chain)
    RouterA — RouterB — RouterC — RouterD
    172.16.1.0/24     (chain links /30)     192.168.4.0/24

    ## Pre-configured (already done)
    - All interface IPs are set and interfaces are up
    - No routing protocol is running

    ## Your Tasks
    1. Configure static routes on ALL routers so every network is reachable.
    2. On RouterA: add a default route pointing to RouterB (10.0.12.2).
    3. On RouterD: add a default route pointing to RouterC (10.0.34.1).
    4. On RouterB and RouterC: add specific static routes for 172.16.1.0/24 and 192.168.4.0/24.
    5. Verify end-to-end connectivity between RouterA's LAN and RouterD's LAN.
    6. Challenge: remove the RouterB–RouterC link and add a floating static route
       with AD=200 as a backup. Verify failover.

    ## Verification
    - `show ip route static` — should list routes on each router
    - `ping 192.168.4.1 source 172.16.1.1` from RouterA should succeed
    """)
    return objectives


@lab('acl_standard', 'acl', 'Standard ACL lab: permit/deny traffic between networks')
def acl_standard(tree):
    devices = {d.findtext('ENGINE/NAME'): d for d in tree.findall('.//DEVICE')}

    set_config(devices['RouterA'], """\
!
hostname RouterA
!
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet0/1
 ip address 10.0.0.1 255.255.255.252
 no shutdown
!
ip route 192.168.2.0 255.255.255.0 10.0.0.2
!
end""")

    set_config(devices['RouterB'], """\
!
hostname RouterB
!
interface GigabitEthernet0/0
 ip address 10.0.0.2 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/1
 ip address 192.168.2.1 255.255.255.0
 no shutdown
!
ip route 192.168.1.0 255.255.255.0 10.0.0.1
!
end""")

    objectives = textwrap.dedent("""\
    # Standard ACL Lab

    ## Topology
    LAN A (192.168.1.0/24) — RouterA — [10.0.0.0/30] — RouterB — LAN B (192.168.2.0/24)

    ## Pre-configured
    - Interface IPs, static routes — full connectivity exists

    ## Your Tasks
    1. Verify pings work between all hosts before adding any ACL.
    2. Create standard ACL 10 on RouterB that DENIES host 192.168.1.100
       and PERMITS all other traffic from 192.168.1.0/24.
    3. Apply the ACL inbound on RouterB's Gig0/0 (the WAN interface).
    4. Verify 192.168.1.100 is blocked but other hosts in 192.168.1.0/24 still work.
    5. Create a named standard ACL called MGMT-BLOCK that denies 192.168.1.0/24
       entirely and permits any. Apply it outbound on RouterA Gig0/1.
    6. Document: what is the implicit rule at the end of every ACL?

    ## Verification
    - `show ip access-lists` — verify ACL entries and hit counts
    - `show ip interface gig0/0` — confirm ACL is applied
    """)
    return objectives


# ── main ──────────────────────────────────────────────────────────────────────

def list_labs():
    print("\nAvailable labs:")
    for name, info in LABS.items():
        print(f"  {name:20} — {info['description']}")
    print()

def generate(lab_name, out_pkt):
    if lab_name not in LABS:
        print(f"Unknown lab: {lab_name}")
        list_labs()
        sys.exit(1)

    info = LABS[lab_name]
    base_xml = BASE_XMLS[info['base']]

    print(f"[*] Loading base topology: {os.path.basename(base_xml)}")
    tree = ET.parse(base_xml)

    print(f"[*] Applying lab: {lab_name}")
    objectives = info['fn'](tree)

    # Write modified XML to temp file
    tmp_xml = out_pkt.replace('.pkt', '_tmp.xml')
    tree.write(tmp_xml, encoding='unicode', xml_declaration=False)

    # Encode to PKT
    ptexplorer = os.path.join(TRACER_DIR, 'ptexplorer.py')
    result = subprocess.run(
        ['python', ptexplorer, '-e', tmp_xml, out_pkt],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("ERROR encoding PKT:", result.stderr)
        sys.exit(1)

    os.remove(tmp_xml)
    print(f"[*] PKT written: {out_pkt}")

    # Write objectives
    obj_file = out_pkt.replace('.pkt', '_objectives.md')
    with open(obj_file, 'w', encoding='utf-8') as f:
        f.write(objectives)
    print(f"[*] Objectives: {obj_file}")
    print()
    print(objectives)

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ('--list', '-l'):
        list_labs()
        sys.exit(0)

    lab_name = sys.argv[1]
    out_pkt = sys.argv[2] if len(sys.argv) > 2 else os.path.join(SCRIPT_DIR, lab_name + '.pkt')
    generate(lab_name, out_pkt)
