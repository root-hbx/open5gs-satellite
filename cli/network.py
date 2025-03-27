#!/usr/bin/env python3

import subprocess
import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

class NetworkConfig:

    def config_network(self):
        """Handle network related operations"""
        print("Configuring network for Open5GS...")
        
        # Must be run as root
        if os.geteuid() != 0:
            logging.error("Error: Network configuration requires root privileges.")
            logging.error("Please run the command with sudo.")
            sys.exit(1)
            
        try:
            logging.info("Enabling IPv4 forwarding...")
            subprocess.run(["sysctl", "-w", "net.ipv4.ip_forward=1"], check=True)
            
            logging.info("Enabling IPv6 forwarding...")
            subprocess.run(["sysctl", "-w", "net.ipv6.conf.all.forwarding=1"], check=True)
            
            logging.info("Configuring IPv4 NAT masquerading...")
            subprocess.run([
                "iptables", "-t", "nat", "-A", "POSTROUTING", 
                "-s", "10.45.0.0/16", "!", "-o", "ogstun", 
                "-j", "MASQUERADE"
            ], check=True)

            logging.info("Configuring IPv6 NAT masquerading...")
            subprocess.run([
                "ip6tables", "-t", "nat", "-A", "POSTROUTING", 
                "-s", "2001:db8:cafe::/48", "!", "-o", "ogstun", 
                "-j", "MASQUERADE"
            ], check=True)

            logging.info("Disable UFW...")
            subprocess.run(["ufw", "disable"], check=True)
            
            print("Network configuration completed successfully.")
            
        except subprocess.SubprocessError as e:
            logging.error(f"Error configuring network: {e}")
            sys.exit(1)

    def create_utun(self):
        """Handle virtual network tunnel creation"""
        print("Creating virtual network tunnel...")
        
        # Must be run as root
        if os.geteuid() != 0:
            logging.error("Error: Virtual tunnel creation requires root privileges.")
            logging.error("Please run the command with sudo.")
            sys.exit(1)
            
        try:
            logging.info("Creating TUN device 'ogstun'...")
            subprocess.run(["ip", "tuntap", "add", "name", "ogstun", "mode", "tun"], check=True)
            
            logging.info("Configuring IPv4 address for ogstun...")
            subprocess.run(["ip", "addr", "add", "10.45.0.1/16", "dev", "ogstun"], check=True)
            
            logging.info("Configuring IPv6 address for ogstun...")
            subprocess.run(["ip", "addr", "add", "2001:db8:cafe::1/48", "dev", "ogstun"], check=True)
            
            logging.info("Activating ogstun interface...")
            subprocess.run(["ip", "link", "set", "ogstun", "up"], check=True)
            
            print("Virtual network tunnel 'ogstun' created and configured successfully.")
            
        except subprocess.SubprocessError as e:
            logging.error(f"Error creating virtual network tunnel: {e}")
            sys.exit(1)

    def delete_utun(self):
        """Handle virtual network tunnel deletion"""
        print("Deleting virtual network tunnel...")

        # Must be run as root
        if os.geteuid() != 0:
            logging.error("Error: Virtual tunnel deletion requires root privileges.")
            logging.error("Please run the command with sudo.")
            sys.exit(1)

        try:
            # Check if the interface exists
            result = subprocess.run(
                ["ip", "link", "show", "ogstun"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False
            )
            
            if result.returncode != 0:
                logging.info("Virtual network tunnel 'ogstun' already deleted. All good!")
                return

            logging.info("Deleting TUN device 'ogstun'...")
            subprocess.run(["ip", "link", "del", "ogstun"], check=True)
            print("Virtual network tunnel 'ogstun' deleted successfully.")

        except subprocess.SubprocessError as e:
            logging.error(f"Error deleting virtual network tunnel: {e}")
            sys.exit(1)
