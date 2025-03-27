# Open5gs for Satellite Networks

This repo is based on [open5gs](https://open5gs.org/) v2.7.4

There are 2 branch:

- `stable`: main branch, ensure stability
- `mm-roam`: nightly built

## Quick Start

**Skeleton**

Follow [Building Open5GS from Sources - Open5GS](https://open5gs.org/open5gs/docs/guide/02-building-open5gs-from-sources/) to configure and build the skeleton:

- Getting MongoDB
- Setting up TUN device (not persistent after rebooting)
- Building Open5GS
  - ensure all tests go smoothly
  - config file: `$open5gs-satellite/build/configs/sample.yaml`
- Configure Open5GS
- Running Open5GS
  - ensure all tests work well
  - config files: `$open5gs-satellite/install/etc/open5gs/[NAME].yaml`
- Building the WebUI of Open5GS

**Roaming Between Core Networks**

Follow [Roaming: Roaming Test on a Single Host](https://open5gs.org/open5gs/docs/tutorial/05-roaming/) to build a simple test:

- Config Home PLMN
- Config Visited PLMN
- Run the V-PLMN 5G Core and H-PLMN 5G Core on a single host
  - Home Network: open multiple windows, keep running for connection
  - Visited Network: open multiple windows, keep running for observation
  - Performs a test of UE access while roaming subscribed to H-PLMN
 
## Development

> For Integrated Space-Terrestrial Network (ISTN)

### End2End TraficGen Instances (Terrestrial)

> Conducting End-to-End Traffic Generation Testing Based on this Framework

For a user equipment (UE) in a 5G core network, we aim to traverse the core network and reach a server in the wide-area network (WAN) to establish a connection and conduct traffic testing.

In this process:

1. Network traffic can be captured and analyzed using **Wireshark** or **Traceroute** to determine the traffic path.  
2. The 5G core network is implemented using **Open5GS**.  
3. The UE can be either an **Open5GS-native component** or simulated using **UERANSIM**.

### End2End TrafficGen Instances (Satellite)

Coming Soon...

### Dynamic CoreNets

Coming Soon...

### High-Frequency Link Establishment

Coming Soon...

### Roaming between Multiple Satellite CoreNets

Coming Soon...
