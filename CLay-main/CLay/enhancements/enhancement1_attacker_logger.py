# enhancement1_attacker_logger.py
# Author: Deepika (DSATM - 2nd Year)
# Logs attacker info (IP + User-Agent) to logs/attackers.log

import os
import datetime

def log_attacker(client_ip, user_agent):
    """
    Logs attacker info (IP + User-Agent) to logs/attackers.log
    """
    log_msg = f"{datetime.datetime.now()} | IP: {client_ip}, Detected Bad User Agent: {user_agent}\n"

    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/attackers.log", "a") as log_file:
            log_file.write(log_msg)
    except Exception as e:
        # Fail silently to avoid terminal output; dashboard reads the log file.
        pass
