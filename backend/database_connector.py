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


def connect(function):
    """
    Decorator to manage database connection and cursor setup.
    :param function: The function to execute with a database connection and cursor.
    :return:
    """

    def wrapper(*args, **kwargs):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**CONFIG)
            if conn.is_connected():
                logging.info("[database_connector-test] Successfully connected to the database.")
                cursor = conn.cursor()
                return function(cursor, conn)
        except mysql.connector.Error as e:
            logging.error('[database_connector-test] Connection error: %s', e)
            raise
        except Exception as e:
            logging.error('[database_connector-test] Unexpected error: %s', e)
            raise e
        finally:
            if cursor:
                cursor.close()
                logging.info("[wrapper] cursor closed.")
            if conn and conn.is_connected():
                conn.close()
                logging.info("[wrapper] connection closed.")

    return wrapper


@connect
def read(cursor, conn):
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(f"[read] {row}")
    return rows


@connect
def write(cursor, conn):
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                   ("Test", "test@test.test", "test"))
    conn.commit()
    logging.info("[database_connector - write] Inserted data into the database.")


if __name__ == "__main__":
    # write()
    read()
