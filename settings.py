"""
In settings.py you can change IPs (e.g. Database / etc.)
- Add multiple IPs to the (connection_routing) dictionary, make sure you don't overwrite previously initialized data.
"""
import os

# List of all available apps to update in-app static files
# (note that the DEFAULT_STATIC_FILE_PATH must be the same)
apps = [
    'main',
    'loginApp',
]

# Database routing
connection_routing = {
    'database': 'localhost',
}

CONFIG = {
    'host': connection_routing['database'],
    'user': 'root',
    'password': '',
    'database': 'neptune_test_db',
}

# to prevent unwanted database operations
allowed_tables = ['users']

# Default paths
DEFAULT_PATH = "HTML_files/"
DEFAULT_STATIC_FILE_PATH = "static_files/"

DEFAULT_PATHS = {
    'error_template': os.path.join(DEFAULT_PATH, 'error_template.html'),
}
