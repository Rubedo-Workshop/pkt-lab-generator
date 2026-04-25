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
