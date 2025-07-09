import sqlite3


class DatabaseConnection:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        print(f"connecting to sqlite3 database: {self.db_name}...")
        try:
            self.conn = sqlite3.connect(self.db_name)
            return self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to the db: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and exc_tb:
            print("Error Occurred:\n", exc_val)
            self.conn.close()
        else:
            self.conn.commit()
            self.conn.close()
        return True


with DatabaseConnection('users.db') as cursor:
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    print(result)
