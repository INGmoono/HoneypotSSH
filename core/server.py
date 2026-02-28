"""
server.py

Basic multi-threaded TCP listener.
This is the foundation for the SSH honeypot server.

Currently:
- Accepts incoming TCP connections
- Spawns a new thread per client
- Prints client IP and port
"""

import socket
import threading

HOST = "0.0.0.0"
PORT = 2222


def handle_client(client_socket, client_address):
    """
    Handles a single client connection.

    Args:
        client_socket (socket.socket): The client socket.
        client_address (tuple): (IP, port) of the client.
    """

    ip, port = client_address
    print(f"[+] New connection from {ip}:{port}")

    # For now, just close the connection
    client_socket.close()


def start_server():
    """
    Starts the TCP server and listens for incoming connections.
    """

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(100)

    print(f"[+] Honeypot listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()

        # Create a new thread per connection
        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address),
            daemon=True
        )

        client_thread.start()