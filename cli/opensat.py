#!/usr/bin/env python3

import sys
import argparse
import logging
import os

from database import handle_database
from network import handle_network
from ps import handle_process_status
from psc import handle_process_control
from clear import handle_cleanup
from utun import handle_utun
from help import show_custom_help
from error import handle_error_cmd

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
    parser.add_argument('-h', '--help', action='store_true', help='Show help information')
    
    # Add subcommands as positional arguments
    subparsers = parser.add_subparsers(dest='command')

    # Add various subcommands: opensat <command>
    db_parser = subparsers.add_parser('db', help='Database operations')
    utun_parser = subparsers.add_parser('utun', help='Create virtual network tunnel')
    net_parser = subparsers.add_parser('net', help='Network operations')
    ps_parser = subparsers.add_parser('ps', help='Process status')
    psc_parser = subparsers.add_parser('psc', help='Process control')
    cls_parser = subparsers.add_parser('cls', help='Cleanup operations')

    # Parse arguments
    args = parser.parse_args()
    
    # Process commands
    if args.help:
        show_custom_help()
    elif args.command == 'db':
        handle_database()
    elif args.command == 'net':
        handle_network()
    elif args.command == 'ps':
        handle_process_status()
    elif args.command == 'psc':
        handle_process_control()
    elif args.command == 'cls':
        handle_cleanup()
    elif args.command == 'utun':
        handle_utun()

if __name__ == "__main__":
    main()
