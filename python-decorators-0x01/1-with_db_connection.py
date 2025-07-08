import sqlite3
import functools


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper_with_db_connection(*args, **kwargs):
        try:
            conn = sqlite3.connect('users.db')
            mutable_args = list(args)
            mutable_args.insert(0, conn)  # insert at index 0
            updated_args = tuple(mutable_args)
        except sqlite3.Error as e:
            print(f"Error connecting to db", {e})
            raise
        result = func(*updated_args, **kwargs)
        conn.close()
        return result
    return wrapper_with_db_connection


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch user by ID with automatic connection handling


user = get_user_by_id(user_id=1)
print(user)
