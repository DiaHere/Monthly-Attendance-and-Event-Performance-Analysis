import mysql.connector
from config import DB_CONFIG 

def get_connection():
    """Open and return a MySQL connection using DB_CONFIG."""
    return mysql.connector.connect(**DB_CONFIG)

def load_data_to_sql(df, table_name, columns, unique_col):

    # get the connection and create the cursor
    conn = get_connection()
    cursor = conn.cursor()

    # the set of dates that are already in the table
    cursor.execute(f"SELECT {unique_col} FROM {table_name};")
    loaded =  {row[0] for row in cursor.fetchall()}

    # convert unique column and its equivlenet in the sql table to string to match the types
    df[unique_col] = df[unique_col].astype(str)
    loaded_str = {str(x) for x in loaded}

    # dates to add that are not in the table
    to_insert = df.loc[~df[unique_col].isin(loaded_str)]

    # SQL code to insert the new rwos into those columns
    placeholders = ','.join(['%s'] * len(columns))
    insert_statment = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"

    # insert the records into the SQL table
    records = to_insert[columns].values.tolist()
    

    if records:
        cursor.executemany(insert_statment, records)
        conn.commit()
        print(f"Inserted {cursor.rowcount} new rows into {table_name}.")
    else:
        print(f"No new rows to add to {table_name}.")
    
    cursor.close()
    conn.close()

