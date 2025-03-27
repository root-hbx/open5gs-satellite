#!/usr/bin/env python3

import logging

def handle_error_cmd():
    '''handle error command'''
    logging.error("\nInvalid input. Please check the command and try again...")

def handle_cleanup():
    """Release all open5gs resources"""
    print("\nExecuting cleanup operations...")

def show_custom_help():
    '''show all functionality for opensat'''
    print("\nUsage: opensat [options]")
    print("\nYour options:")
    print("  -h, help              Show all functionality")
    print("  -v, version           Show version")
    print("  db                    Database operation")
    print("  utun                  Create virtual network tunnel")
    print("  net                   Network operation")
    print("  ps                    Show all open5gs process status")
    print("  psc                   Open5gs process control")
    print("  cls                   Clear all open5gs resources")
    print()

def show_version_info():
    print("\nOpenSAT version 0.1.0")
    print("Copyright (C) 2025 OpenSat Boxuan Hu")
    print()

