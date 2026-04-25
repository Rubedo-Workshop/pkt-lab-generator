# Lab Objectives

## 1. Static Routing Fundamentals
Route 10.164.28.0/24 and 10.7.189.0/24 across WAN 198.71.62.0/30 using static routes.

Objectives:
- Assign 10.164.28.1 to RouterA G0/0/0 (LAN A: 10.164.28.0/24) and 10.7.189.1 to RouterB G0/0/0 (LAN B: 10.7.189.0/24).
- Ping from SiteAHost (10.164.28.50) to SiteBHost (10.7.189.50) to verify end-to-end connectivity.
- Assign 198.71.62.1 to RouterA G0/0/1 and 198.71.62.2 to RouterB G0/0/1 (WAN subnet 198.71.62.0/30).
- On RouterA, add a static route for 10.7.189.0/24 via 198.71.62.2. On RouterB, add a static route for 10.164.28.0/24 via 198.71.62.1.
- Set SiteAHost default gateway to 10.164.28.1 and SiteBHost default gateway to 10.7.189.1.

Notes:
All devices start unconfigured. Assign IPs and static routes from scratch.
