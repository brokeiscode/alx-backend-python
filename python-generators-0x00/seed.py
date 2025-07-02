import mysql.connector as db_connector
from mysql.connector import Error
import csv

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'ALX_prodev'


def connect_db():
    # connects to the mysql database server
    """
    Connects to the MySQL database
    :return: db_connector.connection.MySQLConnection or None
    """
    try:
        connection = db_connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        connection.commit()
    except Error as e:
        print(f"Error checking/creating database '{DB_NAME}': {e}")
        return None
    finally:
        cursor.close()


def connect_to_prodev():
    # connects the ALX_prodev database in MYSQL
    """
    Connects to the MySQL database
    :return: db_connector.connection.MySQLConnection or None
    """
    try:
        connection = db_connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    cursor = connection.cursor()
    try:
        # Create a table if it doesn't exist
        create_table_query = """
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            )"""
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error while creating/checking table: {e}")


def insert_data(connection, data):
    cursor = connection.cursor()
    csv_file_path = data
    insert_query = """
                   INSERT INTO user_data (name, email, age) VALUES (%s, %s, %s)
                       """
    try:
        # Inserts data in the database if it does not exist
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            for row in reader:
                cursor.execute(insert_query, (row[0], row[1], row[2]))
            connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error while Inserting data: {e}")
