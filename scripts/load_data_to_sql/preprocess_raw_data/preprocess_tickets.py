import pandas as pd 
from datetime import datetime
import os

# Load the CSV
# credit refunded data
def load_csv_tickets():
    current_dir = os.path.dirname(__file__)        
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
    
    file_path = os.path.join(project_root, '..', 'data_raw', 'Tickets.csv')
    return pd.read_csv(file_path)

def preprocess_df_tickets():
    df_tickets = load_csv_tickets()

    # Convert the date column to a datetime format
    df_tickets['date_range'] = pd.to_datetime(df_tickets['Accounting Date'], format = '%m/%d/%Y')

    # Drop columns that are null and not needed anymore
    df_tickets.drop(columns = ['Accounting Date','Stock Item Name','Amount','Total Received'], inplace = True)

    # Remove the zeros and no payment rows - meaning there was no ticket purchase
    temp = (df_tickets['masked_column'] == 0) & (df_tickets['Item Payment Type'] == "No Payment")
    df_tickets.drop(df_tickets[temp].index, inplace=True)

    # Rename columns to match the sql table
    df_tickets.rename(columns={"masked_column": "ticket_prices", "Item Payment Type": "payment_type","Event Name": "event_title"}, inplace = True)

    return df_tickets