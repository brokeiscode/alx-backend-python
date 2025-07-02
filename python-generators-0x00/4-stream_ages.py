from mysql.connector import Error
import seed


def stream_user_ages():
    try:
        connection = seed.connect_to_prodev()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT age FROM user_data')
            for row in cursor:
                yield row['age']
            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error streaming users age: {e}")


def calc_average_age():
    divider = 0
    sum_of_ages = 0
    for age in stream_user_ages():
        if not age:
            break
        sum_of_ages += age
        divider += 1
    average_age = sum_of_ages / divider if divider > 0 else 0
    print(f"Average age of users: {average_age:.2f}")


if __name__ == '__main__':
    calc_average_age()
