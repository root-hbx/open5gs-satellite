# Roaming Test on a Single Host

[official doc](https://open5gs.org/open5gs/docs/tutorial/05-roaming/)

## Home PLMN

(1) Create h-nrf.yaml (replace with your own path)

```sh
sh -c 'cat << EOF > ./install/etc/open5gs/h-nrf.yaml
logger:
  file:
    path: /home/open5gs/open5gs/install/var/log/open5gs/h-nrf.log # replace with your own path
#  level: info   # fatal|error|warn|info(default)|debug|trace

global:
  max:
    ue: 1024  # The number of UE can be increased depending on memory size.
#    peer: 64

nrf:
  serving:  # 5G roaming requires PLMN in NRF
    - plmn_id:
        mcc: 999
        mnc: 70
  sbi:
    server:
      - address: nrf.5gc.mnc070.mcc999.3gppnetwork.org
EOF'
```

(2) Update h-scp.yaml (replace with your own path)

```sh
sh -c 'cat << EOF > ./install/etc/open5gs/h-scp.yaml
logger:
  file:
    path: /home/acetcom/Documents/git/open5gs/install/var/log/open5gs/h-scp.log
#  level: info   # fatal|error|warn|info(default)|debug|trace

global:
  max:
    ue: 1024  # The number of UE can be increased depending on memory size.
#    peer: 64

scp:
  sbi:
    server:
      - address: 127.0.1.200
        port: 7777
    client:
      nrf:
        - uri: http://nrf.5gc.mnc070.mcc999.3gppnetwork.org
EOF'
```

(3) Update ausf.yaml

prev:

```yaml
ausf:
  sbi:
    server:
      - address: 127.0.0.11
        port: 7777
    client:
#      nrf:
#        - uri: http://127.0.0.10:7777
      scp:
        - uri: http://127.0.0.200:7777
```

modified:

```yaml
ausf:
  sbi:
    server:
      - address: ausf.5gc.mnc070.mcc999.3gppnetwork.org
      # - address: 127.0.0.11
        # port: 7777
    client:
#      nrf:
#        - uri: http://127.0.0.10:7777
      scp:
        - uri: http://127.0.1.200:7777
        # - uri: http://127.0.0.200:7777
```

(4) Update udm.yaml

prev:

```yaml
  sbi:
    server:
      - address: 127.0.0.12
        port: 7777
    client:
#      nrf:
#        - uri: http://127.0.0.10:7777
      scp:
        - uri: http://127.0.0.200:7777
```

modified:

```yaml
  sbi:
    server:
      - address: udm.5gc.mnc070.mcc999.3gppnetwork.org
      # - address: 127.0.0.12
        # port: 7777
    client:
#      nrf:
#        - uri: http://127.0.0.10:7777
      scp:
        - uri: http://127.0.1.200:7777
        # - uri: http://127.0.0.200:7777
```

(5) Update udr.yaml

prev:

```yaml
udr:
  sbi:
    server:
      - address: 127.0.0.20
        port: 7777
    client:
#      nrf:
#        - uri: http://127.0.0.10:7777
      scp:
        - uri: http://127.0.0.200:7777
```

modified:

```yaml
udr:
  sbi:
    server:
      - address: 127.0.0.20
        port: 7777
    client:
#      nrf:
#        - uri: http://127.0.0.10:7777
      scp:
        - uri: http://127.0.1.200:7777
        # - uri: http://127.0.0.200:7777
```

(6) Update sepp1.yaml

prev:

```yaml
  sbi:
    server:
      - address: 127.0.1.250
        port: 7777
    client:
#      nrf:
#        - uri: http://127.0.0.10:7777
      scp:
        - uri: http://127.0.0.200:7777
```

modified:

```yaml
  sbi:
    server:
      - address: 127.0.1.250
        port: 7777
    client:
#      nrf:
#        - uri: http://127.0.0.10:7777
      scp:
        - uri: http://127.0.1.200:7777
        # - uri: http://127.0.0.200:7777
```

## Visited PLMN

(1) Update nrf.yaml

prev:

```yaml
nrf:
  serving:  # 5G roaming requires PLMN in NRF
    - plmn_id:
        mcc: 999
        mnc: 70
```

modified:

```yaml
nrf:
  serving:  # 5G roaming requires PLMN in NRF
    - plmn_id:
        mcc: 001 # 999
        mnc: 01 # 70
```

(2) Update amf.yaml

prev:

```yaml
amf:
  sbi:
    server:
      - address: 127.0.0.5
        port: 7777
    client:
#      nrf:
#        - uri: http://127.0.0.10:7777
      scp:
        - uri: http://127.0.0.200:7777
  ngap:
    server:
      - address: 127.0.0.5
  metrics:
    server:
      - address: 127.0.0.5
        port: 9090
  guami:
    - plmn_id:
        mcc: 999
        mnc: 70
      amf_id:
        region: 2
        set: 1
  tai:
    - plmn_id:
        mcc: 999
        mnc: 70
      tac: 1
  plmn_support:
    - plmn_id:
        mcc: 999
        mnc: 70
      s_nssai:
        - sst: 1
  security:
    integrity_order : [ NIA2, NIA1, NIA0 ]
    ciphering_order : [ NEA0, NEA1, NEA2 ]
  network_name:
    full: Open5GS
    short: Next
  amf_name: open5gs-amf0
  time:
#    t3502:
#      value: 720   # 12 minutes * 60 = 720 seconds
    t3512:
      value: 540    # 9 minutes * 60 = 540 seconds
```

modified:

```yaml
amf:
  sbi:
    server:
      - address: 127.0.0.5
        port: 7777
    client:
#      nrf:
#        - uri: http://127.0.0.10:7777
      scp:
        - uri: http://127.0.0.200:7777
  ngap:
    server:
      - address: 127.0.2.5
      # - address: 127.0.0.5
  metrics:
    server:
      - address: 127.0.0.5
        port: 9090
  access_control:
    - plmn_id:
        mcc: 001
        mnc: 01
    - plmn_id:
        mcc: 999
        mnc: 70
  guami:
    - plmn_id:
        mcc: 001 #999
        mnc: 01 #70
      amf_id:
        region: 2
        set: 1
  tai:
    - plmn_id:
        mcc: 001 #999
        mnc: 01 #70
      tac: 1
  plmn_support:
    - plmn_id:
        mcc: 001 #999
        mnc: 01 #70
      s_nssai:
        - sst: 1
  security:
    integrity_order : [ NIA2, NIA1, NIA0 ]
    ciphering_order : [ NEA0, NEA1, NEA2 ]
  network_name:
    full: Open5GS
    short: Next
  amf_name: open5gs-amf0
  time:
#    t3502:
#      value: 720   # 12 minutes * 60 = 720 seconds
    t3512:
      value: 540    # 9 minutes * 60 = 540 seconds
```

(3) Update pcf.yaml

prev:

```yaml
# db_uri: mongodb://localhost/open5gs
logger:
  file:
    path: /home/open5gs/open5gs-satellite/install/var/log/open5gs/pcf.log
#  level: info   # fatal|error|warn|info(default)|debug|trace

global:
  max:
    ue: 1024  # The number of UE can be increased depending on memory size.
#    peer: 64

pcf:
  sbi:
    server:
      - address: 127.0.0.13
        port: 7777
    client:
#      nrf:
#        - uri: http://127.0.0.10:7777
      scp:
        - uri: http://127.0.0.200:7777
  metrics:
    server:
      - address: 127.0.0.13
        port: 9090

policy:
  - plmn_id:
      mcc: 999
      mnc: 70
    slice:
      - sst: 1  # 1,2,3,4
        default_indicator: true
        session:
          - name: internet
            type: 3  # 1:IPv4, 2:IPv6, 3:IPv4v6
            ambr:
              downlink:
                value: 1
                unit: 3  # 0:bps, 1:Kbps, 2:Mbps, 3:Gbps, 4:Tbps
              uplink:
                value: 1
                unit: 3
            qos:
              index: 9  # 1, 2, 3, 4, 65, 66, 67, 75, 71, 72, 73, 74, 76, 5, 6, 7, 8, 9, 69, 70, 79, 80, 82, 83, 84, 85, 86
              arp:
                priority_level: 8  # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
                pre_emption_vulnerability: 1  # 1: Disabled, 2:Enabled
                pre_emption_capability: 1  # 1: Disabled, 2:Enabled
```

modified:

```yaml
b_uri: mongodb://localhost/open5gs # uncomment!
logger:
  file:
    path: /home/open5gs/open5gs-satellite/install/var/log/open5gs/pcf.log
#  level: info   # fatal|error|warn|info(default)|debug|trace

global:
  max:
    ue: 1024  # The number of UE can be increased depending on memory size.
#    peer: 64

pcf:
  sbi:
    server:
      - address: 127.0.0.13
        port: 7777
    client:
#      nrf:
#        - uri: http://127.0.0.10:7777
      scp:
        - uri: http://127.0.0.200:7777
  metrics:
    server:
      - address: 127.0.0.13
        port: 9090

policy:
  - plmn_id:
      mcc: 999
      mnc: 70
    slice:
      - sst: 1  # 1,2,3,4
        default_indicator: true
        session:
          - name: internet
            type: 3  # 1:IPv4, 2:IPv6, 3:IPv4v6
            ambr:
              downlink:
                value: 1
                unit: 3  # 0:bps, 1:Kbps, 2:Mbps, 3:Gbps, 4:Tbps
              uplink:
                value: 1
                unit: 3
            qos:
              index: 9  # 1, 2, 3, 4, 65, 66, 67, 75, 71, 72, 73, 74, 76, 5, 6, 7, 8, 9, 69, 70, 79, 80, 82, 83, 84, 85, 86
              arp:
                priority_level: 8  # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
                pre_emption_vulnerability: 1  # 1: Disabled, 2:Enabled
                pre_emption_capability: 1  # 1: Disabled, 2:Enabled
```

## Run the V-PLMN 5G Core and H-PLMN 5G Core on a single host

**Home Network**

5G Core requires root privileges as it uses reserved ports such as http(80) or https(443).

```sh
sudo ./install/bin/open5gs-nrfd -c ./install/etc/open5gs/h-nrf.yaml
./install/bin/open5gs-scpd -c ./install/etc/open5gs/h-scp.yaml
sudo ./install/bin/open5gs-ausfd
sudo ./install/bin/open5gs-udmd
./install/bin/open5gs-udrd
./install/bin/open5gs-seppd -c ./install/etc/open5gs/sepp1.yaml
```

**Visited Network**

```sh
./install/bin/open5gs-nrfd
./install/bin/open5gs-scpd
./install/bin/open5gs-amfd
./install/bin/open5gs-smfd
./install/bin/open5gs-upfd
./install/bin/open5gs-pcfd
./install/bin/open5gs-bsfd
./install/bin/open5gs-nssfd
./install/bin/open5gs-seppd -c ./install/etc/open5gs/sepp2.yaml
```

**Performs a test of UE access while roaming subscribed to H-PLMN**

```sh
$ ./build/tests/registration/registration -c ./build/configs/examples/gnb-001-01-ue-999-70.yaml simple-test
```

