#!/usr/bin/env python3

import logging

from database import Database
from network import NetworkConfig
from ps import ProcessConfig

def handle_error_cmd():
    '''handle error command'''
    logging.error("\nInvalid input. Please check the command and try again...")

def init_sys():
    #TODO(bxhu): add init system
    pass

def handle_cleanup():
    """Release all open5gs resources"""
    print("Cleaning up all open5gs resources...")

    logging.info("==================================================================")
    logging.info("Cleaning up open5gs network interfaces...")
    logging.info("==================================================================")
    net_ins = NetworkConfig()
    net_ins.delete_utun()

    print()

    logging.info("==================================================================")
    logging.info("Cleaning up open5gs processes...")
    logging.info("==================================================================")
    ps_ins = ProcessConfig()
    ps_ins.clear_all_process()

    print()

    logging.info("==================================================================")
    logging.info("Cleaning up open5gs database...")
    logging.info("==================================================================")
    db_ins = Database()
    db_ins.clear_mongodb()
    
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
    print("  net                   Network operation")
    print("  ps                    Show all open5gs process status")
    print("  psc                   Open5gs process control")
    print("  cls                   Clear all open5gs resources (ps, tunnel, db)")
    print()

def show_version_info():
    '''show version info and copyright'''
    print("\nOpenSAT version 0.1.0")
    print("Copyright (C) 2025 OpenSat Boxuan Hu")
    print()

