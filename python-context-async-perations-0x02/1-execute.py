import sqlite3

db_name = 'users.db'


class ExecuteQuery:
    def __init__(self, query: str, age: int):
        self.query = query
        self.age = age
        self.conn = None
        self.result = None

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(db_name)
            cursor = self.conn.cursor()
            cursor.execute(self.query, (self.age,))
            self.result = cursor.fetchall()
            return self.result
        except sqlite3.Error as e:
            print(f"Error Executing query:\n {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and exc_tb:
            print("Error Occurred:\n", exc_val)
            self.conn.close()
        else:
            self.conn.commit()
            self.conn.close()
        return True


query = "SELECT * FROM users WHERE age > ?"

with ExecuteQuery(query, 25) as res:
    print(res)
