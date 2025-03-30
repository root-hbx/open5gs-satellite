#!/usr/bin/env python3

import subprocess
import sys
import os
import logging

OPENSAT_CWD = "/home/open5gs/open5gs-satellite"

logging.basicConfig(level=logging.INFO, format='%(message)s')

class ProcessConfig:
    """Configuration for process operations"""

    def show_process_status(self):
        print("Showing Open5GS process status...")
        
        try:
            result = subprocess.run(
                "ps -aux | grep open5gs",
                shell=True, # support shell commands
                check=True,
                text=True,
                capture_output=True
            )

            if result.stdout:
                print(result.stdout)
            else:
                print("No Open5GS processes found running.")
                print("We are ready to go!")
                
        except subprocess.SubprocessError as e:
            logging.error(f"Error showing process status: {e}")
            sys.exit(1)


    def clear_all_process(self):
        """Terminate all Open5GS processes"""
        print("Terminating all Open5GS processes...")
        
        # Must run as root
        if os.geteuid() != 0:
            logging.error("Error: Terminating processes requires root privileges.")
            logging.error("Please run the command with sudo.")
            sys.exit(1)

        open5gs_processes = [
            "open5gs-mmed", "open5gs-sgwcd", "open5gs-smfd", "open5gs-amfd",
            "open5gs-sgwud", "open5gs-upfd", "open5gs-hssd", "open5gs-pcrfd",
            "open5gs-nrfd", "open5gs-scpd", "open5gs-seppd", "open5gs-ausfd",
            "open5gs-udmd", "open5gs-pcfd", "open5gs-nssfd", "open5gs-bsfd",
            "open5gs-udrd"
        ]
        
        try:
            terminated_count = 0
            
            for process in open5gs_processes:
                logging.info(f"Terminating {process}...")
                try:
                    subprocess.run(["pkill", "-9", process], check=False)
                    terminated_count += 1
                except subprocess.SubprocessError as e:
                    logging.warning(f"Warning: Failed to terminate {process}: {e}")
            
            logging.info(f"Process cleanup completed. Attempted to terminate {terminated_count} processes.")

            logging.info("Verifying process termination...")
            result = subprocess.run(
                ["ps", "-aux", "|", "grep", "open5gs"],
                shell=True,
                check=False,
                text=True,
                capture_output=True
            )
            
            # Check if any Open5GS processes are still running
            if "open5gs" in result.stdout and not all(p in result.stdout for p in ["grep", "defunct"]):
                logging.warning("Warning: Some Open5GS processes may still be running:")
                print(result.stdout)
            else:
                logging.info("All Open5GS processes have been terminated successfully.")
                
        except Exception as e:
            logging.error(f"Error during process cleanup: {e}")
            sys.exit(1)


    def start_all_process(self):
        """Start all Open5GS service processes"""
        print("Starting all Open5GS processes...")
        
        # Get current working directory and change to Open5GS directory
        print("[Switching to OpenSat directory]")
        current_dir = os.getcwd() # current path
        os.chdir(OPENSAT_CWD) # switch to OPENSAT_CWD to execute Open5GS processes

        # Define processes to start in sequence
        process_list = [
            "./install/bin/open5gs-nrfd",
            "./install/bin/open5gs-scpd",
            ["./install/bin/open5gs-seppd", "-c", "./install/etc/open5gs/sepp1.yaml"],
            "./install/bin/open5gs-amfd",
            "./install/bin/open5gs-smfd",
            "./install/bin/open5gs-upfd",
            "./install/bin/open5gs-ausfd",
            "./install/bin/open5gs-udmd", 
            "./install/bin/open5gs-pcfd",
            "./install/bin/open5gs-nssfd",
            "./install/bin/open5gs-bsfd",
            "./install/bin/open5gs-udrd",
            "./install/bin/open5gs-mmed",
            "./install/bin/open5gs-sgwcd",
            "./install/bin/open5gs-sgwud",
            "./install/bin/open5gs-hssd",
            "./install/bin/open5gs-pcrfd"
        ]
        
        successful_count = 0
        
        try:
            for process in process_list:
                if isinstance(process, list):
                    # for [list] formed processes
                    proc_name = os.path.basename(process[0])
                    cmd = process
                else:
                    # for string formed processes
                    proc_name = os.path.basename(process)
                    cmd = [process]
                    
                logging.info(f"Starting {proc_name}...")
                try:
                    # Use Popen to create background processes
                    subprocess.Popen(
                        cmd,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        start_new_session=True
                    )
                    
                    successful_count += 1
                    
                    # Add short delay to ensure sequential startup
                    subprocess.run(["sleep", "0.5"], check=False)
                    
                except subprocess.SubprocessError as e:
                    logging.error(f"Warning: Unable to start {proc_name}: {e}")
            
            logging.info(f"Processes startup complete. Successfully started {successful_count} / 17 processes.")
        except Exception as e:
            logging.error(f"Error during process startup: {e}")
            sys.exit(1)
        finally:
            # Restore original working directory
            print("[Back to current directory]")
            os.chdir(current_dir)
