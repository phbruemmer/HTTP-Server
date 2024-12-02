"""
In settings.py you can change IPs (e.g. Database / etc.)
- Add multiple IPs to the (connection_routing) dictionary, make sure you don't overwrite previously initialized data.
"""

connection_routing = {
    'database': ('192.168.115.200', 1443),
}


allowed_tables = ['users']
