# End2End TrafficGen Instances (Terrestrial)

> Conducting End-to-End Terrestrial Traffic Generation Testing Based on OpenSat

For a user equipment (UE) in a 5G core network, we aim to traverse the core network and reach a server in the wide-area network (WAN) to establish a connection and conduct traffic testing.

In this process:

1. Network traffic can be captured and analyzed using **Wireshark** or **Traceroute** to determine the traffic path.  
2. The 5G core network is implemented using **Open5GS**.  
3. The UE can be either an **Open5GS-native component** or simulated using **UERANSIM**.

## Environments and Devices

**Coding Repo**

- [open5gs-satellite](https://github.com/root-hbx/open5gs-satellite): independent
- [ueransim-satellite](https://github.com/root-hbx/ueransim-satellite): independent
- [free5gc](https://github.com/root-hbx/free5gc): forked

**Physical Machine** 

Linux bxhu-ThinkBook-16-G4-IAP Ubuntu24.04LTS

**Virtual Machine**

VMware Workstation 17

- VM1: for open5gs
    - `open5gs@open5gs`: installed with [open5gs-satellite](https://github.com/root-hbx/open5gs-satellite)
    - Memory: 12GB
    - Processors: 8
    - Network Adapter 1: NAT
    - Network Adapter 2: Host-Only
- VM2: for UERANSIM
    - `ueransim@ueransim`: installed with [ueransim-satellite](https://github.com/root-hbx/ueransim-satellite)
    - Memory: 4GB
    - Processors: 2
    - Network Adapter 1: NAT
    - Network Adapter 2: Host-Only
- VM3: just for test
    - `free5gc@free5gc`: installed with [free5gc](https://github.com/root-hbx/free5gc)
    - Memory: 2GB
    - Processors: 2
    - Network Adapter 1: NAT
    - Network Adapter 2: Host-Only

**Network Interfaces**

- VM1: `open5gs@open5gs`
    - ens33: `172.16.162.137`
        - NAT Interface, for data transfer with WAN
    - ens37: `172.16.122.135`
        - Host-only Interface, for connection on the same physical machine
- VM2: `ueransim@ueransim`
    - ens33: `172.16.162.134`
        - NAT Interface, for data transfer with WAN
    - ens34: `172.16.122.133`
        - Host-only Interface, for connection on the same physical machine
- VM3: `free5gc@free5gc`
    - ens33: `172.16.162.135`
        - NAT Interface, for data transfer with WAN
    - ens34: `172.16.122.131`
        - Host-only Interface, for connection on the same physical machine

## Architecture

![alt text](./image/end2end-ter-1.png)

When UERANSIM connecting with Open5gs, there are 2 main links:

1. N2: with AMF (5G control layer)
2. N3: with UPF (5G data layer)

Hence, there are 2 main configurations:

1. gNodeB
    - `vim open5gs-satellite/etc/open5gs/amf.yaml`
    - `vim ~/UERANSIM/config/open5gs-gnb.yaml`
    - test with `build/nr-gnb -c config/open5gs-gnb.yaml`
2. UE
    - `vim open5gs-satellite/etc/open5gs/upf.yaml`
    - test with `sudo build/nr-ue -c config/open5gs-ue.yaml`

## Walkthrough

```sh
# open5gs-satellite
cd open5gs-satellite
git checkout tcpgen
# ueransim-satellite
cd ueransim-satellite
git checkout open5gs
```

### Part 1: gNodeB Config

**(1) vim open5gs-satellite/etc/open5gs/amf.yaml**

Prev:

```yaml
ngap:
    server:
      - address: 127.0.0.5
```

Modified:

```yaml
ngap:
    server:
      - address: 172.16.122.135 # ens37 (HostOnly) of open5gs machine
```

**(2) vim ~/UERANSIM/config/open5gs-gnb.yaml**

Prev:

```yaml
linkIp: 127.0.0.1   # gNB's local IP address for Radio Link Simulation (Usually same with local IP)
ngapIp: 127.0.0.1   # gNB's local IP address for N2 Interface (Usually same with local IP)
gtpIp: 127.0.0.1    # gNB's local IP address for N3 Interface (Usually same with local IP)

# List of AMF address information
amfConfigs:
  - address: 127.0.0.5
    port: 38412
```

Modified:

```yaml
linkIp: 172.16.122.133   # ens34 (HostOnly) of ueransim machine
ngapIp: 172.16.122.133   # ens34 (HostOnly) of ueransim machine
gtpIp: 172.16.122.133    # ens34 (HostOnly) of ueransim machine

# List of AMF address information
amfConfigs:
  - address: 172.16.122.135 # ens37 (HostOnly) of open5gs machine
    port: 38412
```

After this, please start all service processes on Open5GS:

```sh
# Prerequisites
cd open5gs-satellite
source activate-opensat
opensat syscls
opensat sysinit
# Start Services (17/17)
./install/bin/open5gs-nrfd
./install/bin/open5gs-scpd
./install/bin/open5gs-seppd -c ./install/etc/open5gs/sepp1.yaml
./install/bin/open5gs-amfd
./install/bin/open5gs-smfd
./install/bin/open5gs-upfd
./install/bin/open5gs-ausfd
./install/bin/open5gs-udmd
./install/bin/open5gs-pcfd
./install/bin/open5gs-nssfd
./install/bin/open5gs-bsfd
./install/bin/open5gs-udrd
./install/bin/open5gs-mmed
./install/bin/open5gs-sgwcd
./install/bin/open5gs-sgwud
./install/bin/open5gs-hssd
./install/bin/open5gs-pcrfd
```

**(3) test**

```sh
cd ueransim-satellite
build/nr-gnb -c config/open5gs-gnb.yaml
```

If the output shows like this, then we are all good in Part 1:

![alt text](./image/end2end-ter-2.png)

### Part 2: UE Config

**(1) vim open5gs-satellite/etc/open5gs/upf.yaml**

Prev:

```yaml
    gtpu:
        server:
            - address: 127.0.0.7
    session:
        - subnet: 10.45.0.0/16
          gateway: 10.45.0.1
```

Modified:

```yaml
    gtpu:
        server:
            - address: 172.16.122.135 # ens37 (HostOnly) of open5gs machine
    session:
        - subnet: 10.45.0.0/16
          gateway: 10.45.0.1
```

**(2) register on Open5GS WebUI**

```sh
cd open5gs-satellite
cd webui
npm run dev
```

Then go to the WebUI, follow [this tutorial (QuickStart: Register Subscriber Information)](https://open5gs.org/open5gs/docs/guide/01-quickstart/) to log in

After this, register with info in `UERANSIM/config/open5gs-ue.yaml`

![alt text](./image/end2end-ter-5.png)

Please be careful, we need `OPc` rather than `OP`!

![alt text](./image/end2end-ter-6.png)

Then click `save`, now we have:

![alt text](./image/end2end-ter-7.png)

Now UE config is okey!

**(3) test**

```sh
cd ueransim-satellite
sudo build/nr-ue -c config/open5gs-ue.yaml
```

Then open a new terminal window, and `ifconfig`

If the output contains `uertun0`, then we are all good in Part 2:

![alt text](./image/end2end-ter-3.png)

### Part 3: Traffic through 5G Core Network

In UERANSIM terminal window (like above), ping a existing server or URL via `uertun0`:

```sh
ping -I uertun0 baidu.com
ping -I uertun0 google.com
ping -I uertun0 172.16.162.135 # ens33 (data-interface) of free5gc on my physical machine
```

If the output shows like this, then we are all good!

![alt text](./image/end2end-ter-4.png)

## Interact with WireShark

- Keep the last 2 terminals running gNB and UE opened.

- Open another terminal and logged in to the UERANSIM VM and run below commands to store the data packets.

```sh
# change ip field with your UERANSIM IP.
# change the file name where you want to store packets.
sudo tcpdump host <ip> -i any -w <file-name>.pcap
# for my config, it's:
sudo tcpdump host 172.16.122.133 -i any -w open5gs-ueransim-1.pcap
```

Then, download the `.pcap` packages to physical machine (by `vscode`, `scp`, .etc)

```sh
ueransim@ueransim:~/ueransim-satellite$ ls
CMakeLists.txt  CONTRIBUTING.md  LICENSE  README.md  build  cmake-build-release  config  makefile  open5gs-ueransim-1.pcap  src  tools
```

After sometime, stop the terminal running `sudo tcpdump host <ip> -i any -w <file-name>.pcap command`.

The packets are stored in the `.pcap` file. Open the downloaded file on physical machine via wireshark. You can see the flow of data packets and protocols used:

![alt text](./image/end2end-ter-8.png)

## Basic Workflow

In fact, it is unnecessary to undergo extensive configuration and testing procedures each time (refer to Walkthrough above). 

Following the initial walkthrough, we have completed the entire configuration and stored these config files in the corresponding branch. 

Subsequently, our workflow is structured as follows:

(1) Prerequisites:

```sh
# open5gs-satellite
cd open5gs-satellite
git checkout tcpgen
# ueransim-satellite
cd ueransim-satellite
git checkout open5gs
```

```sh
# window 0: init and register
# on open5gs VM
# - initialize for system
source activate-opensat
opensat syscls
opensat sysinit
# - register for UE
cd webui
npm run dev
```

(2) Test and get `uertun0`:

```sh
# window 1: all open5gs services
# on open5gs VM
./install/bin/open5gs-nrfd
./install/bin/open5gs-scpd
./install/bin/open5gs-seppd -c ./install/etc/open5gs/sepp1.yaml
./install/bin/open5gs-amfd
./install/bin/open5gs-smfd
./install/bin/open5gs-upfd
./install/bin/open5gs-ausfd
./install/bin/open5gs-udmd
./install/bin/open5gs-pcfd
./install/bin/open5gs-nssfd
./install/bin/open5gs-bsfd
./install/bin/open5gs-udrd
./install/bin/open5gs-mmed
./install/bin/open5gs-sgwcd
./install/bin/open5gs-sgwud
./install/bin/open5gs-hssd
./install/bin/open5gs-pcrfd
```

```sh
# window 2:
# on ueransim VM
cd ueransim-satellite
build/nr-gnb -c config/open5gs-gnb.yaml
```

```sh
# window 3:
# on ueransim VM
cd ueransim-satellite
sudo build/nr-ue -c config/open5gs-ue.yaml
```

```sh
# window 4:
# on ueransim VM
ifconfig
# you can also use wireshark here ;)
```

