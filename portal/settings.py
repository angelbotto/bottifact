"""Configuration validation shared by the portal and setup CLI."""
import re
from urllib.parse import urlsplit


def validate_origin(origin):
    parsed = urlsplit(origin)
    if (parsed.scheme not in ('http', 'https') or not parsed.hostname
            or parsed.username or parsed.password or parsed.path not in ('', '/')
            or parsed.query or parsed.fragment
            or not re.fullmatch(r'[A-Za-z0-9.\-:\[\]]+', parsed.netloc)):
        raise ValueError('Use an HTTP(S) origin without credentials, paths or special characters.')
    # Accessing port also rejects malformed or out-of-range ports.
    if parsed.port == 0:
        raise ValueError('Use a valid port.')
    if parsed.scheme == 'http' and parsed.hostname not in ('localhost', '127.0.0.1', '::1'):
        raise ValueError('Remote origins require HTTPS. HTTP is only supported on loopback.')
    return origin.rstrip('/')
