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
    :param position: column position (eg. id / username / email / password -> 0 / 1 / 2 / 3)
    :return: True if item exists in the database.
    """
    valid_value = False
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        if value == row[position]:
            valid_value = True
    return valid_value


@connect
def get_id(cursor, conn, table, column, value, cleaned=False, force_clean=False):
    """
    gets the id of a table entry in the database.
    :param force_clean: returns first element
    :param cleaned: cleans the output when set to true
    :param cursor: -
    :param conn: -
    :param table: table name (string)
    :param column: column name (string)
    :param value: Value to look for
    :return: id (integer)
    """
    query = f"SELECT id FROM {table} WHERE {column} = %s"
    cursor.execute(query, (value,))

    result = cursor.fetchall()
    if result:
        logging.info(f"[get_id] ID found: {result}")
        if cleaned and not force_clean:
            new_result = []
            for i in result:
                new_result.append(i[0])
            result = new_result
        if force_clean:
            result = result[0][0]
        return result
    else:
        logging.info(f"[get_id] No ID found.")
        return None


@connect
def get_by_id(cursor, conn, table, entry_id):
    """
    :param cursor: -
    :param conn: -
    :param table: name of the table (string)
    :param entry_id: id (integer)
    :return: full entry from id
    """
    query = f"SELECT * FROM {table} WHERE id = %s"
    cursor.execute(query, (entry_id,))
    result = cursor.fetchone()
    if result:
        logging.info("[get_by_id] Entry found: %s", result[0])
        return result
    else:
        logging.info("[get_by_id] No Entry found.")
        return None


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
    done = False
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
        done = True
    except mysql.connector.Error as e:
        logging.error("[remove] mysql error - No table / index found: %s", e)
        raise
    except Exception as e:
        logging.error("[remove] unexpected error: %s", e)
        raise
    finally:
        return done


@connect
def read(cursor, conn, table, printable=False):
    """
    Reads the users database table.
    :param table: table name (string)
    :param printable: prints out the rows
    :param cursor: -
    :param conn: -
    :return:
    """
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    if printable:
        for row in rows:
            print(f"[read] {row}")
    return rows


@connect
def write(cursor, conn, table, value):
    """
    Writes data into the users database table
    :param table: table name in the database (string)
    :param value: Value to add to the database (tuple)
    :param cursor: -
    :param conn: -
    :return:
    """
    pos = 1
    for val in value:
        if validate(val, pos):
            logging.error("[write] Could not write data without creating duplicates.")
            return
        pos += 1

    cursor.execute(f"INSERT INTO {table} (username, email, password) VALUES (%s, %s, %s)", value)
    conn.commit()
    logging.info("[database_connector - write] Inserted data into the database.")


if __name__ == "__main__":
    write("users", ("test", "test@test.test", "test"))
    exit_code = remove("users", get_id('users', 'username', 'test1', force_clean=True))
    print(exit_code)
    get_id(table="users", column="username", value="test")
    test = get_by_id("users", 10)
    # print(test)
    valid = validate("Test", 1)
