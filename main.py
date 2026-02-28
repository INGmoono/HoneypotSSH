"""
main.py

Entry point for the SSH Honeypot.

Current stage:
- Loads persistent SSH host key
- Starts multi-threaded TCP listener
"""

from core.key_manager import load_or_generate_host_key
from core.server import start_server


def main():
    """
    Initializes honeypot components.
    """

    load_or_generate_host_key()
    start_server()


if __name__ == "__main__":
    main()