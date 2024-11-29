import mysql.connector
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'test',
}

try:
    connection = mysql.connector.connect(**CONFIG)

    if connection.is_connected():
        logging.info("[database_connector-test] Successfully connected to the database.")
        # DB Tasks here
except mysql.connector.Error as e:
    logging.error('[database_connector-test] Connection error: %s', e)
except Exception as e:
    logging.error('[database_connector-test] Unexpected error: %s', e)
finally:
    if connection.is_connected():
        connection.close()
        logging.info("[database_connector-test] Database connection closed.")
