"""
geoip.py

Handles geolocation lookups for attacker IP addresses.

Uses the public API from ip-api.com to retrieve:

- Country
- City
- Latitude
- Longitude
- ISP
- ASN
"""

import requests


def get_ip_info(ip):
    """
    Retrieves geolocation information for a given IP address.

    Parameters
    ----------
    ip : str
        The IP address to query.

    Returns
    -------
    dict or None
        Dictionary containing geolocation data or None if lookup fails.
    """

    try:
        # API endpoint for IP geolocation
        url = f"http://ip-api.com/json/{ip}"

        # Send request to API
        response = requests.get(url, timeout=3)

        # Convert response to JSON
        data = response.json()

        # If lookup failed
        if data["status"] != "success":
            return None

        # Extract relevant information
        return {
            "country": data.get("country"),
            "city": data.get("city"),
            "lat": data.get("lat"),
            "lon": data.get("lon"),
            "isp": data.get("isp"),
            "asn": data.get("as"),
        }

    except Exception:
        # Fail silently to avoid crashing honeypot
        return None

        