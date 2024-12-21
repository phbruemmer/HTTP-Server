from backend.database import database_connector as dc
import random
import hashlib


def create():
    while True:
        session_value = random.randint(0, pow(2, 512))
        hash_object = hashlib.sha256()
        hash_object.update(str(session_value).encode())
        hash_hex = hash_object.hexdigest()
        check_db_value = dc.get_id('users', 'session_id', hash_hex)
        if check_db_value is None:
            break
    return session_value, hash_hex


if __name__ == "__main__":
    print(create())
