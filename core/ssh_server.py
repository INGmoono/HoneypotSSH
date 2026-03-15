"""
ssh_server.py

Implements a fake SSH server using Paramiko.
Captures authentication attempts and logs them persistently.
"""

from core.analytics import (
    register_attempt,
    get_top_usernames,
    get_top_passwords,
    is_suspicious,
    render_stats
)

import paramiko
from core.logger import log_attack
from core.geoip import get_ip_info


class SSHHoneypotServer(paramiko.ServerInterface):
    """
    Custom SSH server interface to intercept authentication attempts.
    """

    def __init__(self, client_ip, client_port, client_version):
        self.client_ip = client_ip
        self.client_port = client_port
        self.client_version = client_version

    def check_auth_password(self, username, password):
        """
        Called when a client attempts password authentication.
        Captures credentials and updates analytics.
        """

        stats = register_attempt(self.client_ip, username, password)

        geo = get_ip_info(self.client_ip)

        attack_data = {
            "ip": self.client_ip,
            "port": self.client_port,
            "username": username,
            "password": password,
            "ssh_client_version": self.client_version,
        }

        log_attack(attack_data)

        # NETWORK INFORMATION

        print("\n================ SSH HONEYPOT ALERT ================\n")
        print("[Network Information]")
        print(f"    IP Address        : {self.client_ip}")
        print(f"    Source Port       : {self.client_port}")
        print(f"    SSH Client        : {self.client_version}")

        # GEOLOCATION INFORMATION
        if geo:
            print("\n[Geolocation]")
            print(f"    Country           : {geo['country']}")
            print(f"    City              : {geo['city']}")
            print(f"    Coordinates       : {geo['lat']}, {geo['lon']}")
            print(f"    ISP               : {geo['isp']}")
            print(f"    ASN               : {geo['asn']}")
        else:
            print("\n[Geolocation]")
            print("    Geolocation data not available")

        # CREDENTIALS CAPTURED
        print("\n[Credentials Captured]")
        print(f"    Username          : {username}")
        print(f"    Password          : {password}")

        # ATTACK STATISTICS
        print("\n[Attack Statistics]")
        print(f"    Attempts from IP  : {stats['attempts_from_ip']}")

        if stats["time_since_last_attempt"] is not None:
            print(f"    Time since last attempt: {stats['time_since_last_attempt']:.2f}s")

        # Detect automation
        if stats["automated"]:
            print("    ⚠ Possible automated brute-force detected")

        # Suspicious IP flag
        if is_suspicious(self.client_ip):
            print(f"    🚨 Suspicious IP flagged: {self.client_ip}")

        print("\n====================================================\n")
        
        # Show statistics every 10 attempts
        if stats["total_attempts"] % 10 == 0:
            render_stats()

            print("\n📊 Honeypot Statistics")

            print("\nTop Usernames:")
            for user, count in get_top_usernames():
                print(f"    {user} : {count}")

            print("\nTop Passwords:")
            for pwd, count in get_top_passwords():
                print(f"    {pwd} : {count}")

        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED