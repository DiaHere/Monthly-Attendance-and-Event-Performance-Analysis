import pandas as pd 
from datetime import datetime
import os

# Load the CSV
# donations data
def load_csv_donations_csv():
    current_dir = os.path.dirname(__file__)        
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
    
    file_path = os.path.join(project_root, '..', 'data_raw', 'donations.csv')
    return pd.read_csv(file_path)

def preprocess_df_donations():
    df_donations = load_csv_donations_csv()

    # Convert the date column to a datetime format
    df_donations['date'] = pd.to_datetime(df_donations['Accounting Date'], format = '%m/%d/%Y')
    df_donations.drop(columns = 'Accounting Date', inplace = True)

    # Rename columns to match the sql table
    df_donations.rename(columns={"masked_column": "donation_received",}, inplace = True)

    return df_donations
