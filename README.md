# OpenSat: Open5gs for Satellite Networks

This repo is based on [open5gs](https://open5gs.org/) v2.7.4

There are 2 branch:

- `stable`: ensure stability
  - all config files are unmodified
  - all func and module tests should be 100/100
- `mm-roam`: nightly built
  - config files are modified with the requirement of 5G Roaming
  - some errors when testing func and modules in Open5GS User's Guide, no worry

## Quick Start

**(1) Skeleton**

Follow [Building Open5GS from Sources - Open5GS](https://open5gs.org/open5gs/docs/guide/02-building-open5gs-from-sources/) to configure and build the skeleton:

- Getting MongoDB
- Setting up TUN device (not persistent after rebooting)
- Building Open5GS
  - ensure all tests go smoothly
  - config file: `$open5gs-satellite/build/configs/sample.yaml`
- Running Open5GS
  - no *Configure Open5gs*, run directly!
  - ensure all tests work well
  - config files: `$open5gs-satellite/install/etc/open5gs/[NAME].yaml`
- Building the WebUI of Open5GS

**(2) Roaming Between Core Networks**

Follow [Roaming: Roaming Test on a Single Host](https://open5gs.org/open5gs/docs/tutorial/05-roaming/) to build a simple test:

- Config Home PLMN
- Config Visited PLMN
- Run the V-PLMN 5G Core and H-PLMN 5G Core on a single host
  - Home Network: open multiple windows, keep running for connection
  - Visited Network: open multiple windows, keep running for observation
  - Performs a test of UE access while roaming subscribed to H-PLMN

**Warning: Something You Should Know Before Conducting Research**

(1) Every time you `git pull`, you need to rebuild the whole system:

```sh
# rebuild
cd open5gs-satellite
meson build --prefix=`pwd`/install
ninja -C build
# test
./build/tests/attach/attach ## EPC Only
./build/tests/registration/registration ## 5G Core Only
# ...
```

(2) Every time you restart your experiment device (PC/VM/Server...), you have to reconfigure the networks:

```sh
sudo ip tuntap add name ogstun mode tun
sudo ip addr add 10.45.0.1/16 dev ogstun
sudo ip addr add 2001:db8:cafe::1/48 dev ogstun
sudo ip link set ogstun up
```

```sh
sudo sysctl -w net.ipv4.ip_forward=1
sudo sysctl -w net.ipv6.conf.all.forwarding=1
sudo iptables -t nat -A POSTROUTING -s 10.45.0.0/16 ! -o ogstun -j MASQUERADE
sudo ip6tables -t nat -A POSTROUTING -s 2001:db8:cafe::/48 ! -o ogstun -j MASQUERADE
```

```sh
sudo ufw disable
```

## Development

For Integrated Space-Terrestrial Network (ISTN), focusing on mobility management of satellite networks.

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

## Contributing

We welcome all contributions to the project! See [CONTRIBUTING](./CONTRIBUTING.md) for how to get involved.
