<h1 align="center">
    OpenSat: Open5gs Simulator for Satellite Networks
</h1>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./docs/opensat.png">
    <img alt="OpenSat" src="./docs/opensat.png" width=25%>
  </picture>
</p>

<p align="center">

<!-- use https://shields.io/badges/git-hub-contributors -->
<!-- <img alt="GitHub Contributors" src="https://img.shields.io/github/contributors/root-hbx/open5gs-satellite"> -->

<a href="https://github.com/root-hbx/open5gs-satellite/blob/mm-roam/docs/exp/start.md">
  <img alt="Documentation" src="https://img.shields.io/badge/docs-gray?logo=readthedocs&logoColor=f5f5f5">
</a>

<!-- use https://shields.io/badges/git-hub-actions-workflow-status -->
<img alt="Workflow Status" src="https://img.shields.io/github/actions/workflow/status/root-hbx/open5gs-satellite/meson-ci.yml">

<a href="https://github.com/root-hbx/open5gs-satellite/issues">
  <img src="https://img.shields.io/github/issues/root-hbx/open5gs-satellite?style=flat&logo=github" alt="Issues">
</a>

<a href="https://github.com/root-hbx/open5gs-satellite/pulls">
  <img src="https://img.shields.io/github/issues-pr/root-hbx/open5gs-satellite?style=flat&logo=github" alt="Pull Requests">
</a>

<!-- use https://shields.io/badges/git-hub-license -->
<img alt="License" src="https://img.shields.io/github/license/root-hbx/open5gs-satellite">

<!-- use https://shields.io/badges/git-hub-repo-stars -->
<img alt="Repo Stars" src="https://img.shields.io/github/stars/root-hbx/open5gs-satellite">

</p>

------

This repo is based on [open5gs](https://open5gs.org/) v2.7.4

Currently, there are several branch:

- `stable`: ensure stability
  - all config files are unmodified
  - all func and module tests should be 100/100
- `mm-roam`: nightly built
  - config files are modified with the requirement of 5G Roaming
  - some errors when testing func and modules in Open5GS User's Guide, no worry
- `tcpgen`: interact with UERANSIM
  - working on "End2End Terrestrial TrafficGen" experiments
- `mm-switch`: 
  - inspired by [#issue 5](https://github.com/root-hbx/open5gs-satellite/issues/5)
  - working on "Dynamic CoreNets" experiments

There are some testing platforms interacting closely with OpenSat:

- [open5gs-satellite](https://github.com/root-hbx/open5gs-satellite): independent
- [ueransim-satellite](https://github.com/root-hbx/ueransim-satellite): independent
- [free5gc](https://github.com/root-hbx/free5gc): forked

## Prerequisites for OpenSat

**Everything you should know about 5G before getting started**

- [5G Network Overwiew && 5G Architecture](./docs/notes/5g-arch.md)
- [Mobility Management](./docs/notes/mm-register.md)
- [5G Roaming (HR and LBO)](./docs/notes/5g-roam.md)
- [Basic Tools for OpenSat](./docs/notes/tools.md)

**Your device should be prepared**

Details can be checked at [pre-opensat doc](./docs/exp/start.md).

## Quick Start

**(0) Prerequisites for OpenSat**

```sh
cd $OPEN5GS_SATELLITE
# create and activate pyvenv for opensat
python3 -m venv .venv
source activate-opensat
# now you can use `opensat` command
opensat -h
```

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

**Warning: Something You Should Know Before Using OpenSat**

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
# initialize opensat system: net | tun | db
opensat sysinit
```

(3) Every time you finish your experiments, please deconstruct all open5gs resources:

```sh
# cleanup all opensat resources: ps | tun | db 
opensat syscls
```

## Schedule

For Integrated Space-Terrestrial Network (ISTN), focusing on mobility management of satellite networks.

Details can be checked [here](./docs/exp/dev.md).

|Experiments|Slide|Jump to|Status|
|:---:|:---:|:---:|:---:|
|Roaming on Single Host|[RoamingSim](https://docs.google.com/presentation/d/1ZVhvkNzKHPul5X0yeQPGms3_eiUkdLPVjTuXveiJAm8/edit?usp=sharing)|[mm-roam branch](https://github.com/root-hbx/open5gs-satellite/tree/mm-roam)|✅|
|End2End TrafficGen Instances (Terrestrial)|[End2End TrafficGen](https://docs.google.com/presentation/d/1_rAwluZDBoHryAtUwrHF48Qy8hf-ipSehQBhtGmoyr4/edit?usp=sharing)|[tcpgen branch](https://github.com/root-hbx/open5gs-satellite/tree/tcpgen)|✅|
|End2End TrafficGen Instances (Satellite)|TBD|TBD|⌛️|
|Dynamic CoreNets|TBD|[mm-switch branch](https://github.com/root-hbx/open5gs-satellite/tree/mm-switch)|👷|
|High-Frequency Link Establishment|TBD|TBD|⌛️|
|Roaming between Multiple Satellite CoreNets|TBD|TBD|⌛️|

## Contributing

We welcome all contributions to the project! See [CONTRIBUTING](./CONTRIBUTING.md) for how to get involved.

Copyright (C) 2025 OpenSat Boxuan Hu <huboxuan2004@gmail.com>
