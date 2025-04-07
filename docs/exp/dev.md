# Development

For Integrated Space-Terrestrial Network (ISTN), focusing on mobility management of satellite networks.

## Roaming on Single Host

> Run the V-PLMN 5G Core and H-PLMN 5G Core on a single host

- Home PLMN
- Visited PLMN

This module is inspired by [official doc @open5gs](https://open5gs.org/open5gs/docs/tutorial/05-roaming/)



## End2End TrafficGen Instances (Terrestrial)

> Conducting End-to-End Traffic Generation Testing Based on OpenSat

For a user equipment (UE) in a 5G core network, we aim to traverse the core network and reach a server in the wide-area network (WAN) to establish a connection and conduct traffic testing.

In this process:

1. Network traffic can be captured and analyzed using **Wireshark** or **Traceroute** to determine the traffic path.  
2. The 5G core network is implemented using **Open5GS**.  
3. The UE can be either an **Open5GS-native component** or simulated using **UERANSIM**.



## End2End TrafficGen Instances (Satellite)

Coming Soon...



## Dynamic CoreNets

> End-to-End Terrestrial Traffic Switching between 2 CoreNets

Based on "End2End TrafficGen Instances (Terrestrial)", now we wanna test traffic switching between different corenets.

In this process:

1. Network traffic can be captured and analyzed using **Wireshark** or **Traceroute** to determine the traffic path.  
2. Two 5G core networks (`open5gs` / `open5gs2`) are implemented using **Open5GS**.  
3. The UE is simulated by **UERANSIM**.

This module is inspired by [#issue 5](https://github.com/root-hbx/open5gs-satellite/issues/5).



## High-Frequency Link Establishment

Coming Soon...



## Roaming between Multiple Satellite CoreNets

Coming Soon...


