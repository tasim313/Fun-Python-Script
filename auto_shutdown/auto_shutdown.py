#!/usr/bin/env python3
import datetime
import pytz
import subprocess
import time
import logging

# Set up logging
logging.basicConfig(
    filename='/var/log/auto_shutdown.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def shutdown_at_2330():
    # Set the timezone to Asia/Dhaka
    dhaka_tz = pytz.timezone('Asia/Dhaka')
    
    while True:
        try:
            # Get current time in Dhaka
            now = datetime.datetime.now(dhaka_tz)
            
            # Check if it's 11:30 PM
            if now.hour == 23 and now.minute == 30:
                logging.info("It's 11:30 PM in Dhaka. Shutting down the system...")
                # Shutdown command for Linux
                subprocess.run(['shutdown', '-h', 'now'])
                break
            
            # Wait for 1 minute before checking again
            time.sleep(60)
        except Exception as e:
            logging.error(f"Error: {e}")
            time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    logging.info("Script started. Will shutdown at 11:30 PM Bangladesh Time.")
    shutdown_at_2330()