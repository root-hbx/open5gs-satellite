#!/usr/bin/env python3

import sys
import argparse
import logging
import os

# Import custom classes
from database import Database
from network import NetworkConfig
from ps import ProcessConfig

# Import custom modules
from others import handle_error_cmd, handle_cleanup, show_custom_help, show_version_info

logging.basicConfig(level=logging.INFO, format='%(message)s')

# Custom ArgumentParser to handle errors and show help
class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        handle_error_cmd()
        show_custom_help()
        sys.exit(2)

def main():
    """
    OpenSat - Open5GS for Satellite Networks
    - This script serves as a command-line interface for OpenSat
    - Handles various operations related to Open5GS
        - database: come to backend mongodb
        - network: NAT and routing
        - utun: create a virtual network tunnel called "ogstun"
        - process status: show all open5gs process status
        - process control: start/stop open5gs process
        - cleanup: release all open5gs resources
    """

    # Use custom argument parser
    parser = CustomArgumentParser(
        description='OpenSat: Open5GS for Satellite Networks',
        prog='opensat',
        add_help=False
    )

    # Add custom arg option: opensat -<arg>
    parser.add_argument('-h', '--help', action='store_true', help='Show help info')
    parser.add_argument('-v', '--version', action='store_true', help='Show version info')

    # Add subcommands as positional arguments
    subparsers = parser.add_subparsers(dest='command')

    # Add various subcommands: opensat <command>
    help_parser = subparsers.add_parser('help', help='Show help info')
    version_parser = subparsers.add_parser('version', help='Show version info')
    db_parser = subparsers.add_parser('db', help='Database operations')
    utun_parser = subparsers.add_parser('utun', help='Create virtual network tunnel')
    net_parser = subparsers.add_parser('net', help='Network operations')
    ps_parser = subparsers.add_parser('ps', help='Process status')
    psc_parser = subparsers.add_parser('psc', help='Process control')
    cls_parser = subparsers.add_parser('cls', help='Cleanup operations')

    # Parse arguments
    args = parser.parse_args()
    
    # Process commands
    if args.help or args.command == 'help':
        # opensat -h/-help/help
        show_custom_help()
    elif args.version or args.command == 'version':
        # opensat -v/-version/version
        show_version_info()
    elif args.command == 'db':
        # opensat db
        db_handler = Database()
        db_handler.handle_database()
    elif args.command == 'net':
        # opensat net
        network_handler = NetworkConfig()
        network_handler.config_network()
    elif args.command == 'utun':
        # opensat utun
        utun_handler = NetworkConfig()
        utun_handler.handle_utun()
    elif args.command == 'ps':
        # opensat ps
        ps_handler = ProcessConfig()
        ps_handler.handle_process_status()
    elif args.command == 'psc':
        # opensat psc
        psc_handler = ProcessConfig()
        psc_handler.handle_process_control()
    elif args.command == 'cls':
        # opensat cls
        handle_cleanup()
    else:
        pass # handled by CustomArgumentParser::error()

if __name__ == "__main__":
    main()
