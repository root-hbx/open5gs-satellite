#!/usr/bin/env python3

import subprocess
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

class Database:

    def _check_mongosh_installed(self):
        try:
            subprocess.run(["mongosh", "--version"], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE, 
                        check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            logging.error("MongoDB Shell (mongosh) not found. Please install MongoDB tools.")
            sys.exit(1)
    
    def open_mongosh(self):
        """Handle mongodb operations."""
        print("Launching MongoDB shell...")
        try:
            subprocess.run(["mongosh"], check=True)
            logging.info("MongoDB shell session completed.")
        except FileNotFoundError:
            logging.error("Error: MongoDB shell (mongosh) not found. Please install MongoDB tools.")
            sys.exit(1)
        except subprocess.SubprocessError as e:
            logging.error(f"Error executing MongoDB shell: {e}")
            sys.exit(1)

    def show_mongodb(self):
        print("Showing subscribers in MongoDB...")
        
        try:
            self._check_mongosh_installed()
            
            mongo_commands = """
            use open5gs
            db.subscribers.find()
            """
            
            process = subprocess.Popen(
                ["mongosh", "--quiet"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(mongo_commands)
            
            if process.returncode != 0:
                logging.error(f"MongoDB command failed: {stderr}")
                sys.exit(1)
            
            if stdout.strip():
                print("\nSubscriber information:")
                print(stdout)
            else:
                print("No subscribers found in the database.")
                
        except Exception as e:
            logging.error(f"Error showing MongoDB data: {e}")
            sys.exit(1)

    def clear_mongodb(self):
        print("Clearing subscribers from MongoDB...")
        
        try:
            self._check_mongosh_installed()
            
            mongo_commands = """
            use open5gs
            print("Current subscribers before deletion:")
            db.subscribers.find()
            print("\\nDropping subscribers collection...")
            db.subscribers.drop()
            print("\\nVerifying subscribers after deletion:")
            db.subscribers.find()
            """
            
            process = subprocess.Popen(
                ["mongosh", "--quiet"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(mongo_commands)
            
            if process.returncode != 0:
                logging.error(f"MongoDB command failed: {stderr}")
                sys.exit(1)
                
            print(stdout)
            logging.info("MongoDB subscribers successfully cleared.")

        except Exception as e:
            logging.error(f"Error clearing MongoDB data: {e}")
            sys.exit(1)

