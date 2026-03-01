"""
logger.py

Handles persistent logging of SSH attack attempts in JSON format.
Each attack is stored as a JSON line for scalability and easy parsing.
"""

import json
import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "attacks.json")


def ensure_log_directory():
    """
    Ensures the logs directory exists.
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)


def log_attack(data: dict):
    """
    Appends a new attack entry to the JSON log file.

    Args:
        data (dict): Attack information dictionary.
    """

    ensure_log_directory()

    # Add timestamp in UTC ISO format
    data["timestamp_utc"] = datetime.utcnow().isoformat()

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")