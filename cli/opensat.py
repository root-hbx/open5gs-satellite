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
from others import handle_error_cmd, handle_cleanup, show_custom_help, show_version_info, init_sys

logging.basicConfig(level=logging.INFO, format='%(message)s')

# Custom ArgumentParser to handle errors and show help
class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        handle_error_cmd()
        show_custom_help()
        sys.exit(2)

def main():
    #TODO(bxhu): add info
    """
    OpenSat - Open5GS for Satellite Networks
    - This script serves as a command-line interface for OpenSat
    - Handles various operations related to Open5GS
        - database: come to backend mongodb
        - network: NAT and routing
        - ctun: create a virtual network tunnel called "ogstun"
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
    dbs_parser = subparsers.add_parser('dbshow', help='Database shell')
    dbc_parser = subparsers.add_parser('dbcls', help='Database cleanup')
    ctun_parser = subparsers.add_parser('ctun', help='Create virtual network tunnel')
    dtun_parser = subparsers.add_parser('dtun', help='Delete virtual network tunnel')
    net_parser = subparsers.add_parser('net', help='Network operations')
    ps_parser = subparsers.add_parser('ps', help='Process status')
    psc_parser = subparsers.add_parser('pscls', help='Process control')
    cls_parser = subparsers.add_parser('syscls', help='Cleanup operations')
    init_parser = subparsers.add_parser('sysinit', help='System initialization')

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
        db_handler.open_mongosh()
    elif args.command == 'dbshow':
        # opensat dbshow
        db_handler = Database()
        db_handler.show_mongodb()
    elif args.command == 'dbcls':
        # opensat dbcls
        db_handler = Database()
        db_handler.clear_mongodb()
    elif args.command == 'net':
        # opensat net
        network_handler = NetworkConfig()
        network_handler.config_network()
    elif args.command == 'ctun':
        # opensat ctun
        ctun_handler = NetworkConfig()
        ctun_handler.create_utun()
    elif args.command == 'dtun':
        # opensat dtun
        dtun_handler = NetworkConfig()
        dtun_handler.delete_utun()
    elif args.command == 'ps':
        # opensat ps
        ps_handler = ProcessConfig()
        ps_handler.show_process_status()
    elif args.command == 'pscls':
        # opensat pscls
        psc_handler = ProcessConfig()
        psc_handler.clear_all_process()
    elif args.command == 'sysinit':
        # opensat sysinit
        init_sys()
    elif args.command == 'syscls':
        # opensat cls
        handle_cleanup()
    else:
        pass # handled by CustomArgumentParser::error()

if __name__ == "__main__":
    main()
