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
            conn = mysql.connector.connect(**settings.CONFIG)
            if conn.is_connected():
                logging.info("[database_connector-test] Successfully connected to the database.")
                cursor = conn.cursor()
                return function(cursor=cursor, conn=conn, *args, **kwargs)
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
def validate(table, value, **kwargs):
    """
    Function to validate values in the database and check for duplicates.
    :param table: Name of the table (string)
    :param value: Value to look for in the db
    :param position: column position (eg. id / username / email / password -> 0 / 1 / 2 / 3)
    :return: True if item exists in the database.
    """
    cursor = kwargs.get('cursor')
    position = kwargs.get('position')
    column_name = kwargs.get('column_name')

    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()

    if position is None and column_name is None:
        raise ValueError('[validate] Must provide either column_name or position.')

    if column_name:
        columns = [description[0] for description in cursor.description]
        if column_name not in columns:
            raise ValueError(f'[validate] "{column_name}" does not exist in table "{table}".')
        position = columns.index(column_name)

    for row in rows:
        if value == row[position]:
            return True
    return False


@connect
def get_id(table, column, value, cleaned=False, force_clean=False, **kwargs):
    """
    gets the id of a table entry in the database.
    :param force_clean: returns first element (no list)
    :param cleaned: cleans the output when set to true (list)
    :param table: table name (string)
    :param column: column name (string)
    :param value: Value to look for
    :return: id (integer)
    """
    cursor = kwargs.get('cursor')

    query = f"SELECT id FROM {table} WHERE {column} = %s"
    cursor.execute(query, (value,))

    result = cursor.fetchall()
    if not result:
        logging.info(f"[get_id] No ID found.")
        return None
    logging.info(f"[get_id] ID found: {result}")
    if cleaned and not force_clean:
        new_result = []
        for i in result:
            new_result.append(i[0])
        result = new_result
    if force_clean:
        result = result[0][0]
    return result


@connect
def get_by_id(table, entry_id, **kwargs):
    """
    :param table: name of the table (string)
    :param entry_id: id (integer)
    :return: full entry from id
    """
    cursor = kwargs.get('cursor')

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
def remove(table, id_value, **kwargs):
    """
    Removes data from specific table with specific item ID ( '*' for all items)
    :param table: table name in the database
    :param id_value: item id
    :return:
    """
    cursor = kwargs.get('cursor')
    conn = kwargs.get('conn')

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
def read(table, printable=False, **kwargs):
    """
    Reads the users database table.
    :param table: table name (string)
    :param printable: prints out the rows
    :return: rows
    """
    cursor = kwargs.get('cursor')

    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    if printable:
        for row in rows:
            print(f"[read] {row}")
    return rows


@connect
def write(table, value, **kwargs):
    """
    Writes data into the users database table
    :param table: table name in the database (string)
    :param value: Value to add to the database (tuple)
    :return:
    """
    cursor = kwargs.get('cursor')
    conn = kwargs.get('conn')

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
    valid = validate("users", "Test", 1)

