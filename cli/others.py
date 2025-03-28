#!/usr/bin/env python3

import logging

from database import Database
from network import NetworkConfig
from ps import ProcessConfig

def handle_error_cmd():
    '''handle error command'''
    logging.error("\nInvalid input. Please check the command and try again...")


def init_sys():
    """Initialize all open5gs resources"""
    print("Initializing all open5gs resources...")

    logging.info("==================================================================")
    logging.info("Creating open5gs network interfaces...")
    logging.info("==================================================================")
    net_ins = NetworkConfig()
    net_ins.config_network() # net config: opensat net
    net_ins.create_utun() # utun config: opensat ctun

    print()

    logging.info("==================================================================")
    logging.info("Restart open5gs database...")
    logging.info("==================================================================")
    db_ins = Database()
    db_ins.clear_mongodb() # clear mongodb: opensat dbcls
    
    print()
    
    print("====================================================")
    print("All open5gs resources have been initialized!")
    print("====================================================")


def cleanup_sys():
    """Release all open5gs resources"""
    print("Cleaning up all open5gs resources...")

    logging.info("==================================================================")
    logging.info("Cleaning up open5gs network interfaces...")
    logging.info("==================================================================")
    net_ins = NetworkConfig()
    net_ins.delete_utun() # utun config: opensat dtun

    print()

    logging.info("==================================================================")
    logging.info("Cleaning up open5gs processes...")
    logging.info("==================================================================")
    ps_ins = ProcessConfig()
    ps_ins.clear_all_process() # ps clear: opensat pscls

    print()

    logging.info("==================================================================")
    logging.info("Cleaning up open5gs database...")
    logging.info("==================================================================")
    db_ins = Database()
    db_ins.clear_mongodb() # mongodb clear: opensat dbcls

    print()
    
    print("====================================================")
    print("All open5gs resources have been cleaned up!")
    print("====================================================")


def show_custom_help():
    '''show all functionality for opensat'''
    print("\nUsage: opensat [options]")
    print("\nYour options:")
    print("  -h, help              Show all functionality")
    print("  -v, version           Show version")
    print("  db                    Into MongoDB Shell")
    print("  dbshow                Open5GS Database Demonstration")
    print("  dbcls                 Open5GS Database Cleanup")
    print("  ctun                  Create virtual network tunnel")
    print("  dtun                  Delete virtual network tunnel")
    print("  net                   Network configuration")
    print("  ps                    Show all open5gs process status")
    print("  pscls                 Open5gs process control")
    print("  sysinit               Initialize all open5gs resources (net, tun, db)")
    print("  syscls                Clear all open5gs resources (ps, tun, db)")
    print()

def show_version_info():
    '''show version info and copyright'''
    print("\nOpenSAT version 0.1.0")
    print("Copyright (C) 2025 OpenSat Boxuan Hu <huboxuan2004@gmail.com>")
    print()

