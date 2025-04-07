# Prerequisites for OpenSat

Prior to cloning this repository and conducting further experiments, it is essential to define the experimental environment and specify the requisite configuration requirements.

## Install VMware Workstation

You need to install VMware Workstation 17 on your laptop.

Given the abundance of relevant tutorials available, details are omitted here due to file limits.

I just provide one tutorial about [VMware 17 Installation](https://blog.bxhu2004.com/BLOG/Linux/vmware-conf/), which is written by myself in Chinese. Sorry for the lack of English version. If time permitted, I will be working on this part in the near future.

## Install and Config 4 VMs

Install 4 virtual machines via VMware Workstation:

### How to install a ubuntu server via VMware

[tutorial (CN)](https://blog.bxhu2004.com/BLOG/Linux/ubuntu-server/)

You should go through the file above to install one ubuntu 20.04 server.

It is strongly advisable to ensure that all configuration details align with those specified below. 

>This consistency will mitigate potential discrepancies during subsequent operations, including issues related to absolute paths.

### VM1: open5gs

Hardware Settings (in VMware dashboard):

- Processors: 8
- Memory: 12GB (The more. the better. 12 is the lower bound)

System: Ubuntu 22.04.5 LTS

Usrname@Hostname: `open5gs@open5gs`

Network Interfaces:

- Network Adapter 1, NAT 
    - ens33, `172.16.162.137`
    - This interface doesn't matter, depends on your DHCP
- Network Adapter 2, Host-Only
    - ens37, `172.16.122.135`
    - It's better to keep the same

```sh
(.venv) open5gs@open5gs:/etc/netplan$ cat 01-netcfg.yaml 
network:
  version: 2
  renderer: networkd
  ethernets:
    ens33:
      dhcp4: true
    ens37:
      dhcp4: no # prev: true
      addresses: [172.16.122.135/24] # prev: nothing this line
```

### VM2: open5gs2

Hardware Settings (in VMware dashboard):

- Processors: 8
- Memory: 12GB (The more. the better. 12 is the lower bound)

System: Ubuntu 22.04.5 LTS

Usrname@Hostname: `open5gs2@open5gs2`

Network Interfaces:

- Network Adapter 1, NAT 
    - ens33, `172.16.162.141`
    - This interface doesn't matter, depends on your DHCP
- Network Adapter 2, Host-Only
    - ens37, `172.16.122.120`
    - It's better to keep the same

```sh
(.venv) open5gs2@open5gs2:/etc/netplan$ cat 01-netcfg.yaml 
network:
  version: 2
  renderer: networkd
  ethernets:
    ens33:
      dhcp4: true
    ens37:
      dhcp4: no # prev: true
      addresses: [172.16.122.120/24] # prev: nothing this line
```

### VM3: free5gc

Hardware Settings (in VMware dashboard):

- Processors: 2
- Memory: 2GB (The more. the better. 2 is the lower bound)

System: Ubuntu 20.04.6 LTS

Usrname@Hostname: `free5gc@free5gc`

Network Interfaces:

- Network Adapter 1, NAT 
    - ens33, `172.16.162.135`
    - This interface doesn't matter, depends on your DHCP
- Network Adapter 2, Host-Only
    - ens34, `172.16.122.131`
    - It's better to keep the same

```sh
free5gc@free5gc:/etc/netplan$ cat 00-installer-config.yaml 
# This is the network config written by 'subiquity'
network:
  ethernets:
    ens33:
      dhcp4: true
    ens34:
      dhcp4: no
      addresses: [172.16.122.131/24]
  version: 2
```

### VM4: ueransim

Hardware Settings (in VMware dashboard):

- Processors: 2
- Memory: 4GB (The more. the better. 4 is the lower bound)

System: Ubuntu 20.04.6 LTS

Usrname@Hostname: `ueransim@ueransim`

Network Interfaces:

- Network Adapter 1, NAT 
    - ens33, `172.16.162.134`
    - This interface doesn't matter, depends on your DHCP
- Network Adapter 2, Host-Only
    - ens34, `172.16.122.133`
    - It's better to keep the same

## How to Start

### OpenSat

Follow [Building Open5GS from Sources](https://open5gs.org/open5gs/docs/guide/02-building-open5gs-from-sources/)

1. Getting MongoDB
2. Setting up TUN device
3. Building Open5GS
4. No need to "Configure Open5GS"
5. Running Open5GS
6. Building the WebUI of Open5GS

I believe these steps are enough for a starter.

### free5gc

Follow ["Build free5GC from scratch"](https://free5gc.org/guide/#advanced-build-free5gc-from-scratch) and work on these:

1. Creating a Ubuntu VM using VMware
2. Creating and Configuring a free5GC VM
3. Build and Install free5GC from source code and Test free5GC

I believe these steps are enough for a starter.

### UERANSIM

Follow [UERANSIM Wiki](https://github.com/aligungr/UERANSIM/wiki)

**TL;DR** I believe [this page](https://github.com/aligungr/UERANSIM/wiki/Installation) is good enough for you to start.

## Notes

(1) check distribution version

```sh
lsb_release -a
```

(2) check kernel info

```sh
uname -a
```

(3) check and update netplan

```sh
cd /etc/netplan
sudo vim [XXX-config].yaml
```

```sh
sudo netplan try
sudo netplan apply
```

(4) see IP/MAC of each interface

```sh
# installed by `sudo apt install net-tools`
ifconfig
```

(5) see status of each interface

```sh
# you can see the UP/DOWN status of each interface
ip addr show
```

(6) see all processes

```sh
ps -aux
ps -aux | grep open5gs
```

(7) open5gs network config

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

sudo ufw disable
```

**Not persistent after rebooting!**

Hence, please run `opensat sysinit` at first, each time you wanna use OpenSat system.

And after you finish the experiments, use `opensat syscls` to cleanup the whole system.
