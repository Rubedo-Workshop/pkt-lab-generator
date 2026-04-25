# PKT Lab Generator

> **Unified tool combining tracketpacin and MCP Packet Tracer Server to generate Cisco Packet Tracer `.pkt` files.**

## 🚀 Quick Start

### Generate your first lab in 30 seconds:

```bash
# Clone this repository (already done)
cd pkt-lab-generator

# Install dependencies (only need Twofish for .pkt encoding)
pip install twofish

# Generate an OSPF lab
python pkt_lab_generator.py scenario ospf_validation -o ospf_lab.pkt

# Open in Cisco Packet Tracer!
```

---

## 📋 Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
  - [CLI Commands](#cli-commands)
  - [Scenario-Based Generation](#scenario-based-generation)
  - [Custom Topology](#custom-topology)
  - [Programmatic API](#programmatic-api)
- [Available Scenarios](#available-scenarios)
- [Examples](#examples)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

**PKT Lab Generator** combines two powerful open-source tools into one seamless workflow:

1. **tracketpacin** - Randomized scenario-based lab generation with 16+ CCNA topics
2. **MCP Packet Tracer Server** - Intelligent topology validation, auto-fixing, and configuration generation

### Key Features

✅ **Generate real `.pkt` files** that open directly in Cisco Packet Tracer  
✅ **16+ pre-built scenarios** covering VLANs, OSPF, NAT, ACLs, STP, etc.  
✅ **Custom topology builder** - define your own networks  
✅ **Automatic validation** - catches errors before they happen  
✅ **Auto-fix capabilities** - corrects cable types, port issues, etc.  
✅ **IOS config generation** - complete router/switch/PC configurations  
✅ **Randomized parameters** - unique IPs, VLANs, subnets every time  
✅ **Reproducible** - use seeds for consistent results  

---

## 🔧 How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                     PKT Lab Generator                       │
│                                                             │
│  1. INPUT                                                   │
│     • Scenario template (tracketpacin)                      │
│     • OR custom specification                               │
│     • OR MCP Server plan                                    │
│                                                             │
│  2. TOPOLOGY BUILD                                          │
│     • Create devices (routers, switches, PCs)               │
│     • Create links (cables, ports)                          │
│     • Randomize IPs, VLANs, subnets                         │
│                                                             │
│  3. VALIDATION & AUTO-FIX (MCP Rules)                       │
│     ✓ Check cable types                                     │
│     ✓ Verify port availability                              │
│     ✓ Validate IP addressing                                │
│     ✓ Auto-fix common issues                                │
│                                                             │
│  4. CONFIG GENERATION                                       │
│     • Router configs (OSPF, EIGRP, RIP, static)             │
│     • Switch configs (VLANs, trunks)                        │
│     • PC configs (DHCP, static IP)                          │
│                                                             │
│  5. EXPORT                                                  │
│     • XML format (Packet Tracer readable)                   │
│     • .pkt binary (Twofish EAX encryption via ptexplorer)   │
│     • Markdown objectives                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Installation

### Prerequisites

- **Python 3.10+**
- **Cisco Packet Tracer 8.2+** (to open generated `.pkt` files)
- **tracketpacin** (included)
- **MCP Packet Tracer Server** (included, for validation rules)

### Setup

```bash
# Navigate to the project directory
cd pkt-lab-generator

# Install Twofish encryption library (required for .pkt encoding)
pip install twofish

# Alternative: use pycryptodome
pip install pycryptodome
```

**That's it!** No additional setup required.

---

## 💻 Usage

### CLI Commands

#### 1. List Available Scenarios

```bash
python pkt_lab_generator.py list-scenarios
```

**Output:**
```
Available scenarios:
  - ospf_validation: OSPF routing protocol lab
  - vlan_inter: Inter-VLAN routing
  - nat_pat: NAT/PAT configuration
  - acl_standard: Standard ACLs
  - stp_rapid: Rapid Spanning Tree Protocol
  ...
```

---

#### 2. Generate from Scenario Template

**Basic usage:**
```bash
python pkt_lab_generator.py scenario ospf_validation -o ospf_lab.pkt
```

**With options:**
```bash
# Specific seed for reproducibility
python pkt_lab_generator.py scenario nat_pat -o nat_lab.pkt --seed 42

# With routing protocol
python pkt_lab_generator.py scenario vlan_inter -o vlan_lab.pkt --routing ospf

# With DHCP enabled
python pkt_lab_generator.py scenario branch_single -o branch_lab.pkt --dhcp

# Specify topology size
python pkt_lab_generator.py scenario campus_core -o campus_lab.pkt --size large
```

---

#### 3. Generate Custom Topology

**Create device specification (`devices.json`):**
```json
[
  {"name": "R1", "device_type": "router"},
  {"name": "R2", "device_type": "router"},
  {"name": "SW1", "device_type": "switch"},
  {"name": "PC1", "device_type": "pc"},
  {"name": "PC2", "device_type": "pc"}
]
```

**Create link specification (`links.json`):**
```json
[
  {
    "dev1": "R1",
    "port1": "GigabitEthernet0/0",
    "dev2": "R2",
    "port2": "GigabitEthernet0/0",
    "cable_type": "eCrossOver"
  },
  {
    "dev1": "R1",
    "port1": "GigabitEthernet0/1",
    "dev2": "SW1",
    "port2": "GigabitEthernet0/1"
  },
  {
    "dev1": "SW1",
    "port1": "FastEthernet0/1",
    "dev2": "PC1",
    "port2": "FastEthernet0"
  }
]
```

**Generate:**
```bash
python pkt_lab_generator.py custom -o custom_lab.pkt \
  --devices devices.json \
  --links links.json \
  --routing ospf \
  --dhcp
```

---

### Programmatic API

For advanced usage, import the generator in your Python scripts:

#### Quick Build Functions

```python
from pkt_lab_generator import quick_build_scenario, quick_build_custom

# Generate from scenario
result = quick_build_scenario(
    scenario_name='ospf_validation',
    output_path='ospf_lab.pkt',
    seed=42,
    routing='ospf'
)

print(f"Generated: {result['pkt']}")
```

```python
# Generate custom topology
result = quick_build_custom(
    devices=[
        {"name": "R1", "device_type": "router"},
        {"name": "SW1", "device_type": "switch"},
        {"name": "PC1", "device_type": "pc"},
    ],
    links=[
        {"dev1": "R1", "port1": "Gig0/0", "dev2": "SW1", "port2": "Gig0/1"},
        {"dev1": "SW1", "port1": "Fa0/1", "dev2": "PC1", "port2": "FastEthernet0"},
    ],
    output_path='simple_lab.pkt',
    routing_protocol='ospf',
    dhcp_enabled=True
)
```

---

#### Full API Control

```python
from pkt_lab_generator import PKTLabGenerator, TopologyPlan, DeviceSpec, LinkSpec

# Create topology plan
plan = TopologyPlan(
    devices=[
        DeviceSpec(name="HQ-RTR", device_type="router", model="2911"),
        DeviceSpec(name="HQ-SW", device_type="switch", model="2960-24TT"),
        DeviceSpec(name="Branch-RTR", device_type="router", model="2911"),
        DeviceSpec(name="HQ-PC1", device_type="pc", dhcp=True),
    ],
    links=[
        LinkSpec(dev1="HQ-RTR", port1="Gig0/0", dev2="HQ-SW", port2="Gig0/1"),
        LinkSpec(dev1="HQ-RTR", port1="Serial0/0/0", dev2="Branch-RTR", port2="Serial0/0/0", cable_type="eSerial"),
        LinkSpec(dev1="HQ-SW", port1="Fa0/1", dev2="HQ-PC1", port2="FastEthernet0"),
    ],
    routing_protocol='ospf',
    dhcp_enabled=True,
    metadata={'purpose': 'WAN lab simulation'}
)

# Build lab
generator = PKTLabGenerator(seed=42)

# Step 1: Load plan
generator.from_spec(plan)

# Step 2: Validate and auto-fix
validation = generator.enhance_with_mcp_rules()
if not validation['valid']:
    print(f"Validation errors: {validation['errors']}")

# Step 3: Generate configs
configs = generator.generate_configs()

# Step 4: Export
generator.export_xml('wan_lab.xml')
generator.export_pkt('wan_lab.xml', 'wan_lab.pkt')

# Or use the one-step full build:
result = generator.full_build('wan_lab.pkt', generate_objectives=True)

print(f"Generated files: {result['xml']}, {result['pkt']}")
```

---

## 📚 Available Scenarios

### Routing Protocols
- `ospf_validation` - OSPF routing configuration
- `eigrp_named` - EIGRP named mode
- `rip_basic` - RIP v2 routing
- `static_routing` - Static routes with floating backups

### Switching & VLANs
- `vlan_inter` - Inter-VLAN routing
- `stp_rapid` - Rapid Spanning Tree Protocol
- `etherchannel` - Link aggregation
- `port_security` - Switch port security

### Network Services
- `dhcp_server` - DHCP configuration
- `nat_pat` - NAT/PAT overload
- `ntp_syslog` - NTP and syslog
- `snmp_monitor` - SNMP monitoring

### Security
- `acl_standard` - Standard ACLs
- `acl_extended` - Extended ACLs
- `nat_acl` - NAT with ACLs

### Infrastructure
- `campus_core` - Campus core design
- `branch_single` - Branch office
- `dual_core` - Dual core redundancy
- `campus_branch` - Campus + branch WAN

### Advanced
- `ipv6_basic` - IPv6 addressing
- `qos_policy` - Quality of Service
- `fhrp_hsrp` - HSRP redundancy
- `ipv6_ospf` - OSPFv3 for IPv6

---

## 🎓 Examples

### Example 1: OSPF Lab

```bash
python pkt_lab_generator.py scenario ospf_validation -o ospf_lab.pkt --seed 42
```

**What you get:**
- 2 routers with OSPF peering
- Point-to-point link
- Loopback interfaces
- Test hosts for connectivity
- Complete IOS configurations

---

### Example 2: Multi-VLAN Campus

```bash
python pkt_lab_generator.py scenario campus_core -o campus.pkt --size large --vlan
```

**What you get:**
- Core and edge switches
- Multiple VLANs with trunking
- FHRP (HSRP) for redundancy
- Management IPs
- DHCP scopes

---

### Example 3: Branch Office with NAT

```bash
python pkt_lab_generator.py scenario branch_single -o branch.pkt --routing ospf --nat
```

**What you get:**
- Branch router with NAT/PAT
- Internal VLAN
- WAN connection
- ACL for traffic filtering

---

### Example 4: Custom Enterprise Network

```python
from pkt_lab_generator import PKTLabGenerator, TopologyPlan, DeviceSpec, LinkSpec

# Design your network
plan = TopologyPlan(
    devices=[
        DeviceSpec(name="Internet-RTR", device_type="router"),
        DeviceSpec(name="Edge-RTR", device_type="router"),
        DeviceSpec(name="Core-SW", device_type="switch"),
        DeviceSpec(name="Users-SW", device_type="switch"),
        DeviceSpec(name="Server-SW", device_type="switch"),
        DeviceSpec(name="Web-Server", device_type="server"),
        DeviceSpec(name="User-PC1", device_type="pc", dhcp=True),
        DeviceSpec(name="User-PC2", device_type="pc", dhcp=True),
    ],
    links=[
        LinkSpec(dev1="Internet-RTR", port1="Gig0/0", dev2="Edge-RTR", port2="Gig0/0"),
        LinkSpec(dev1="Edge-RTR", port1="Gig0/1", dev2="Core-SW", port2="Gig0/1"),
        LinkSpec(dev1="Core-SW", port1="Gig0/2", dev2="Users-SW", port2="Gig0/1"),
        LinkSpec(dev1="Core-SW", port1="Gig0/3", dev2="Server-SW", port2="Gig0/1"),
        LinkSpec(dev1="Server-SW", port1="Fa0/1", dev2="Web-Server", port2="FastEthernet0"),
        LinkSpec(dev1="Users-SW", port1="Fa0/1", dev2="User-PC1", port2="FastEthernet0"),
        LinkSpec(dev1="Users-SW", port1="Fa0/2", dev2="User-PC2", port2="FastEthernet0"),
    ],
    routing_protocol='ospf',
    dhcp_enabled=True,
    vlan_config={
        'vlans': {
            10: 'Users',
            20: 'Servers',
            99: 'Management'
        },
        'management_ip': '192.168.99.10'
    },
    metadata={'purpose': 'Enterprise simulation'}
)

# Build
generator = PKTLabGenerator()
generator.from_spec(plan)
generator.full_build('enterprise.pkt')
```

---

## 🏗️ Architecture

### Directory Structure

```
pkt-lab-generator/
├── pkt_lab_generator.py        # Main integration tool
├── examples.py                 # Quick start examples
├── example_devices.json        # Sample device spec
├── example_links.json          # Sample link spec
├── tracketpacin/               # Scenario-based lab generator
│   ├── core.py                 # Lab class, XML generation
│   ├── ptexplorer.py           # .pkt binary encoder (Twofish EAX)
│   ├── scenarios.py            # Scenario library
│   ├── layouts.py              # Topology layouts
│   ├── profiles.py             # Device config profiles
│   └── test.xml                # Packet Tracer XML template
└── MCP_Packet_Tracer/          # MCP validation & configs
    └── src/
        └── packet_tracer_mcp/
            ├── domain/
            │   ├── services/
            │   │   ├── orchestrator.py      # Topology planning
            │   │   ├── validator.py         # Validation rules
            │   │   ├── auto_fixer.py        # Auto-correction
            │   │   └── ip_planner.py        # IP addressing
            │   └── rules/
            │       ├── device_rules.py      # Device validation
            │       ├── cable_rules.py       # Cable validation
            │       └── ip_rules.py          # IP validation
            └── infrastructure/
                └── generator/
                    └── ptbuilder_generator.py  # Script generation
```

### Data Flow

```
User Input (scenario/custom)
         ↓
Topology Planner
         ↓
Device & Link Creation
         ↓
MCP Validation Engine
         ↓ (auto-fix if needed)
Configuration Generator
         ↓
XML Export (via tracketpacin.core.Lab)
         ↓
PKT Binary (via ptexplorer.py Twofish EAX)
         ↓
Cisco Packet Tracer (.pkt file)
```

---

## 🔍 Troubleshooting

### Issue: "Twofish implementation is required"

**Solution:**
```bash
pip install twofish
# OR
pip install pycryptodome
```

---

### Issue: "test.xml not found"

**Solution:** The `test.xml` template file is required from tracketpacin. Ensure the `tracketpacin/` directory is in the same folder as `pkt_lab_generator.py`.

---

### Issue: Generated .pkt won't open in Packet Tracer

**Possible causes:**
1. **Version mismatch** - Ensure you're using Packet Tracer 8.2+
2. **Corrupted encoding** - Try with `--legacy` flag (for PT < 7.3)
3. **Invalid topology** - Check validation output

**Debug:**
```bash
# Generate XML only (skip .pkt encoding)
python pkt_lab_generator.py scenario ospf_validation -o ospf_lab.xml

# Manually open XML in Packet Tracer and check for errors
```

---

### Issue: "No scenarios available"

**Solution:** Ensure `scenarios.py` from tracketpacin is present and contains the `SCENARIO_LIBRARY` dictionary.

---

### Issue: Device positions overlap

**Solution:** Positions are auto-adjusted, but you can specify custom positions:

```python
DeviceSpec(name="R1", device_type="router", position=(300, 150))
```

---

## 📝 License

This project integrates:
- **tracketpacin** (MIT License)
- **MCP Packet Tracer Server** (MIT License)
- **ptexplorer** (MIT License)

---

## 🤝 Contributing

Contributions welcome! Areas of improvement:
- More scenario templates
- Enhanced validation rules
- Better auto-fix algorithms
- Multi-vendor support (Nokia, Arista)
- GUI interface

---

## 📧 Support

For issues with:
- **Scenario generation** → Check tracketpacin docs
- **MCP validation** → Check MCP Packet Tracer docs
- **Packet Tracer compatibility** → Cisco Networking Academy

---

## 🎉 Credits

Built by combining:
- **tracketpacin** by AlexSvobo - https://github.com/AlexSvobo/tracketpacin
- **MCP Packet Tracer Server** by Deiviidsito - https://github.com/Deiviidsito/MCP_Packet_Tracer
- **ptexplorer** by axcheron - https://github.com/axcheron/ptexplorer

---

**Happy networking! 🌐🔧**
