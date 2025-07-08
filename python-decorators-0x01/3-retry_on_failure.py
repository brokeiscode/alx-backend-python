import time
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


def retry_on_failure(retries=3, delay=2):
    def decorator_retry_on_failure(func):
        @functools.wraps(func)
        def wrapper_retry_on_failure(*args, **kwargs):
            for _ in range(retries):
                try:
                    result = func(*args, **kwargs)
                    return result
                except sqlite3.Error:
                    time.sleep(delay)
                    print(delay)
        return wrapper_retry_on_failure
    return decorator_retry_on_failure


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# attempt to fetch users with automatic retry on failure


users = fetch_users_with_retry()
print(users)
