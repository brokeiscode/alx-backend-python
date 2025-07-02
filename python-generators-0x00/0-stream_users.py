from mysql.connector import Error
import seed


def stream_users():
    try:
        connection = seed.connect_to_prodev()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM user_data")
            for row in cursor:
                yield row
            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error streaming data from MySQL: {e}")
