import pandas as pd
import mysql.connector
from config import DB_CONFIG 
import os

# Load the CSV
# Attendance Performance data
def load_csv():
    # __file__ is .../load_data/attendance_loader.py
    base_dir = os.path.dirname(__file__)                       # .../load_data
    project_root = os.path.abspath(os.path.join(base_dir, os.pardir))  
    # project_root → .../

    file_path = os.path.join(project_root, '..', 'data_raw', 'attendance_performance_data.csv')
    df_attendance = pd.read_csv(file_path)

    # Clean the data
    # Change the date column to a date format
    df_attendance['date'] = pd.to_datetime(df_attendance['date'], format='%m/%y').dt.strftime('%m-%d-%y')

    # return the dataframe
    return df_attendance

def get_connection():
    """Open and return a MySQL connection using DB_CONFIG."""
    return mysql.connector.connect(**DB_CONFIG)

def already_loaded(cursor):
    """Return a set of month_year dates already in the table."""
    cursor.execute("SELECT month_year FROM attendance;")
    return {row[0] for row in cursor.fetchall()}

def insert_attendance_data(df):

    # get the connection and create the cursor
    conn = get_connection()
    cursor = conn.cursor()

    loaded = already_loaded(cursor)

    # months to add that are not in attendance 
    to_insert = df.loc[df['date'].isin(loaded)]

    # SQL code to insert the new rwos into those columns
    insert_data = """
        INSERT INTO attendance (
        month_year,
        total_days_in_use,
        num_sep_events,
        total_unique_patrons,
        total_attendance,
        total_first_time_visitors
        )
        VALUES (%s, %s, %s, %s, %s, %s);
    """

    # Insert the records into the attendance table
    records = to_insert.values.tolist()
    cursor.executemany(insert_data, records)

    conn.commit()

    if records != []:
        print(f"Inserted {cursor.rowcount} new rows.")
    else: 
        print('There is no new rows to add')

    cursor.close()
    conn.close()

