import mysql.connector
import logging

# !NOT IMPORTANT FOR THIS FILE!
# The locals() function returns a dictionary containing all the variables and their values that are
# declared in the current scope.
# !NOT IMPORTANT FOR THIS FILE!

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


class Database:
    def connect(self, function):
        """
        Connects to the Database
        :param function: Function to execute database tasks.
        :return:
        """
        try:
            with mysql.connector.connect(**CONFIG) as conn:
                if conn.is_connected():
                    logging.info("[database_connector-test] Successfully connected to the database.")
                    with conn.cursor() as cursor:
                        function(cursor)
        except mysql.connector.Error as e:
            logging.error('[database_connector-test] Connection error: %s', e)
            raise
        except Exception as e:
            logging.error('[database_connector-test] Unexpected error: %s', e)
            raise e

    def read(self):
        pass

    def write(self):
        pass
