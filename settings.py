"""
In settings.py you can change IPs (e.g. Database / etc.)
- Add multiple IPs to the (connection_routing) dictionary, make sure you don't overwrite previously initialized data.
"""
import os

connection_routing = {
    'database': 'localhost',
}

allowed_tables = ['users']

DEFAULT_PATH = "files/"

DEFAULT_PATHS = {
    'error_template': os.path.join(DEFAULT_PATH, 'error_template.html'),
}
