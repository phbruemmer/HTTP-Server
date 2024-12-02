import mysql.connector
import logging
import settings

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
                return function(cursor, conn, *args, **kwargs)
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
def validate(cursor, conn, value, position):
    """
    Function to validate values in the database and check for duplicates.
    :param cursor: -
    :param conn: -
    :param value: Value to look for in the db
    :param position: column position (eg. username / email / password -> 0 / 1 / 2)
    :return: True if item exists in the database.
    """
    valid = False
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    print(rows)
    for row in rows:
        if value in row[position]:
            valid = True
    return valid



@connect
def remove(cursor, conn, table, id_value):
    """
    Removes data from specific table with specific item ID ( '*' for all items)
    :param cursor: -
    :param conn: -
    :param table: table name in the database
    :param id_value: item id
    :return:
    """
    if table not in settings.allowed_tables:
        logging.error("[remove] Could not remove the table / items - Not in allowed list in settings.py")
        return

    try:
        logging.info(f"[remove] removing {id_value} in {table}")
        query = f"DELETE FROM {table}"
        if id_value == "*":
            logging.warning(f"[remove] deleting all rows from {table}!")
            cursor.execute(query)
        else:
            query += " WHERE id = %s"
            cursor.execute(query, (id_value,))
        conn.commit()
    except mysql.connector.Error as e:
        logging.error("[remove] mysql error - No table / index found: %s", e)
        raise
    except Exception as e:
        logging.error("[remove] unexpected error: %s", e)
        raise


@connect
def read(cursor, conn):
    """
    Reads the users database table.
    :param cursor:
    :param conn:
    :return:
    """
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(f"[read] {row}")
    return rows


@connect
def write(cursor, conn, value):
    """
    Writes data into the users database table
    :param value:
    :param cursor:
    :param conn:
    :return:
    """
    pos = 0
    for val in value:
        if validate(val, pos):
            logging.error("[write] Could not write data without creating duplicates.")
            return
        pos += 1

    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", value)
    conn.commit()
    logging.info("[database_connector - write] Inserted data into the database.")


if __name__ == "__main__":
    read()
    write(("Test", "test@test.test", "test"))
    write(("Test1", "test1@test.test", "test1"))
    write(("Test2", "test2@test.test", "test2"))

    remove("users", 1)

    valid = validate("Test", 0)
    print(valid)
