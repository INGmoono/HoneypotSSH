"""
server.py

TCP listener that wraps incoming connections into a Paramiko SSH transport.
"""

import socket
import threading
import paramiko
import time

from core.key_manager import load_or_generate_host_key
from core.ssh_server import SSHHoneypotServer
from core.geoip import get_ip_info

HOST = "0.0.0.0"
PORT = 2222


def handle_client(client_socket, client_address):
    """
    Handles an incoming SSH client connection.
    """

    ip, port = client_address
    print(f"[+] SSH connection from {ip}:{port}")

    transport = None

    try:
        transport = paramiko.Transport(client_socket)

        host_key = load_or_generate_host_key()
        transport.add_server_key(host_key)

        
        server = SSHHoneypotServer(ip, port, None)

        # start negociation SSH
        transport.start_server(server=server)

        # Get hacker's remote SSH version 
        client_version = transport.remote_version
        server.client_version = client_version

        print(f"[+] Client version: {client_version}")

        # wate canal request
        channel = transport.accept(20)

        if channel is None:
            print(f"[!] No channel request from {ip}")
            return

        # keep conection on
        while transport.is_active():
            time.sleep(1)

    except Exception as e:
        print(f"[!] Error handling client {ip}: {e}")

    finally:
        if transport:
            transport.close()
        client_socket.close()

def start_server():
    """
    Starts the multi-threaded SSH honeypot.
    """

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(100)

    print(f"[+] SSH Honeypot listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()

        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address),
            daemon=True
        )

        client_thread.start()