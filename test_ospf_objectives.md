# Lab Objectives

## 1. OSPF Validation
Variant Dual Router Shared LAN: OSPF process 36 across 192.164.28.0/29 and 192.7.189.0/30 with loopback 172.24.125.58.

Objectives:
- Enable OSPF process 36 on both routers. Advertise all connected networks in area 0.
- Assign IP 192.7.189.1 to RouterA G0/0/1 and 192.7.189.2 to RouterB G0/0/1 (subnet 192.7.189.0/30).
- Assign IP 192.164.28.1 to RouterA G0/0/0 and 192.164.28.2 to RouterB G0/0/0 (subnet 192.164.28.0/29).
- Set the point-to-point link network type to point-to-point on both ends.
- Change the OSPF cost on one interface so traffic prefers the alternate path, then check the routing table to confirm the change took effect.

Notes:
All interfaces start unconfigured. Assign IPs, enable OSPF, bring up adjacencies, and test end-to-end reachability. Variant: Dual Router Shared LAN.
