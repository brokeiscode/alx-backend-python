import time
import sqlite3
import functools


query_cache = {}


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper_with_db_connection(*args, **kwargs):
        global query_cache
        cache_key = kwargs['query']
        if cache_key in query_cache:  # Check cache before database connection
            return query_cache[cache_key]
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


def cache_query(func):
    @functools.wraps(func)
    def wrapper_cache_query(*args, **kwargs):
        global query_cache
        cache_key = kwargs['query']
        if cache_key not in query_cache:
            query_cache[cache_key] = func(*args, **kwargs)
        return query_cache[cache_key]
    return wrapper_cache_query


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
