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


def transactional(func):
    @functools.wraps(func)
    def wrapper_transactional(*args, **kwargs):
        conn = args[0]
        try:
            result = func(*args, **kwargs)
            conn.commit()
            print("Transaction committed")
            return result
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Transaction rolled back because of an error \n", e)
    return wrapper_transactional


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?",
                   (new_email, user_id))

# Update user's email with automatic transaction handling


update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
