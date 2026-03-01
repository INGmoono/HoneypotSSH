"""
ssh_server.py

Implements a fake SSH server using Paramiko.
Captures authentication attempts and logs them persistently.
"""

import paramiko
from core.logger import log_attack


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
        """

        attack_data = {
            "ip": self.client_ip,
            "port": self.client_port,
            "username": username,
            "password": password,
            "ssh_client_version": self.client_version,
        }

        log_attack(attack_data)

        print("\n[!] Login attempt detected")
        print(f"    IP: {self.client_ip}")
        print(f"    Username: {username}")
        print(f"    Password: {password}")
        print(f"    Client Version: {self.client_version}")

        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED