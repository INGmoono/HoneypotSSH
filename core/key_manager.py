"""
key_manager.py

Handles SSH host key generation and persistent storage.

This module ensures that the honeypot always uses a consistent
RSA host key across restarts, mimicking real SSH server behavior.
"""

import os
from paramiko import RSAKey


# Path where the SSH host key will be stored
KEY_PATH = "keys/server_rsa.key"


def load_or_generate_host_key():
    """
    Loads an existing RSA host key from disk.

    If the key does not exist, a new 2048-bit RSA key
    is generated and saved persistently.

    Returns:
        RSAKey: The loaded or newly generated host key.
    """

    # Ensure the keys directory exists
    if not os.path.exists("keys"):
        os.makedirs("keys")

    # Load existing key if present
    if os.path.exists(KEY_PATH):
        host_key = RSAKey(filename=KEY_PATH)
        print("[+] Existing RSA host key loaded.")

    else:
        print("[!] No existing host key found.")
        print("[*] Generating new 2048-bit RSA host key...")

        # Generate new RSA key
        host_key = RSAKey.generate(2048)

        # Save key persistently
        host_key.write_private_key_file(KEY_PATH)

        print("[+] New RSA host key generated and saved.")

    return host_key