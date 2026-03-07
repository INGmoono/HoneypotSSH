"""
analytics.py

Real-time analytics engine for the SSH honeypot.

Tracks:
- Attempts per IP
- Time between attempts
- Most common usernames
- Most common passwords
- Suspicious automation detection
"""

from collections import defaultdict, Counter
import json
import os
import time

LOG_FILE = "logs/attacks.json"

# Number of attempts per IP
attempts_per_ip = defaultdict(int)

# Last attempt timestamp per IP
last_attempt_time = {}

# Global counters
username_counter = Counter()
password_counter = Counter()

# Suspicious IP tracking
suspicious_ips = set()

# Global attempt counter
total_attempts = 0


def register_attempt(ip, username, password):
    """
    Registers an attack attempt and updates statistics.
    """

    global total_attempts
    total_attempts += 1

    current_time = time.time()

    attempts_per_ip[ip] += 1

    # Calculate time between attempts
    time_diff = None
    if ip in last_attempt_time:
        time_diff = current_time - last_attempt_time[ip]

    last_attempt_time[ip] = current_time

    # Count username/password usage
    username_counter[username] += 1
    password_counter[password] += 1

    # Detect automation
    automated = False
    if time_diff is not None and time_diff < 1:
        automated = True
        suspicious_ips.add(ip)

    return {
        "attempts_from_ip": attempts_per_ip[ip],
        "time_since_last_attempt": time_diff,
        "automated": automated,
        "total_attempts": total_attempts
    }


def get_top_usernames(n=5):
    """Return most common usernames."""
    return username_counter.most_common(n)


def get_top_passwords(n=5):
    """Return most common passwords."""
    return password_counter.most_common(n)


def is_suspicious(ip):
    """Check if an IP has been flagged as suspicious."""
    return ip in suspicious_ips

def render_stats():
    """
    Displays honeypot statistics in a formatted console box.
    """

    top_users = get_top_usernames()
    top_passwords = get_top_passwords()

    print("\n┌─────────────────────────────────────┐")
    print("│        SSH HONEYPOT STATS           │")
    print("├─────────────────────────────────────┤")

    print("\nTop Usernames")
    for i, (user, count) in enumerate(top_users, start=1):
        print(f"{i}. {user:<12} ({count})")

    print("\nTop Passwords")
    for i, (pwd, count) in enumerate(top_passwords, start=1):
        print(f"{i}. {pwd:<12} ({count})")

    print(f"\nTotal Attempts: {total_attempts}")

    print("\n└─────────────────────────────────────┘\n")

def load_existing_stats():
    """
    Rebuild analytics from the existing JSON log file.
    This allows stats to persist across honeypot restarts.
    """

    global total_attempts

    if not os.path.exists(LOG_FILE):
        return

    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                attack = json.loads(line)

                ip = attack.get("ip")
                username = attack.get("username")
                password = attack.get("password")

                attempts_per_ip[ip] += 1
                username_counter[username] += 1
                password_counter[password] += 1

                total_attempts += 1

            except json.JSONDecodeError:
                continue