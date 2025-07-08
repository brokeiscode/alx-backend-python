import sqlite3
import functools
from datetime import datetime

# decorator to lof SQL queries


def log_queries(func):
    # log the query before executing
    @functools.wraps(func)
    def wrapper_log_queries(*args, **kwargs):
        time = datetime.now()
        for arg in args:
            print(time, '- ' + arg + "\n")
        for key, value in kwargs.items():
            print(time, '- ' + key + ': ' + value + "\n")
        return func(*args, **kwargs)
    return wrapper_log_queries


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
