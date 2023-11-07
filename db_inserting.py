# db_inserting.py
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn_string = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server={os.getenv('DB_SERVER')};Database={os.getenv('DB_NAME')};"
        f"Uid={os.getenv('DB_USER')};Pwd={os.getenv('DB_PASS')};"
    )
    return pyodbc.connect(conn_string)

def store_in_db(data, conn):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO YourTableName (ColumnName) VALUES (?)", data)
    conn.commit()
    cursor.close()
