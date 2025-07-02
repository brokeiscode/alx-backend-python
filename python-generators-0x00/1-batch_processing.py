from mysql.connector import Error
import seed


def stream_users_in_batches(batch_size):
    try:
        connection = seed.connect_to_prodev()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM user_data')
            while True:
                rows = cursor.fetchmany(batch_size)
                if not rows:
                    break  # rows finished
                yield rows
            cursor.close()
            connection.close()
            return rows
    except Error as e:
        print(f"Error streaming data from MySQL: {e}")


def batch_processing(batch_size):
    for rows in stream_users_in_batches(batch_size):
        for user in rows:
            if user.get('age') > 25:
                print(user)
