import pandas as pd 
from datetime import datetime
import os

# Load the CSV
# credit refunded data
def load_csv_credits_refunds():
    current_dir = os.path.dirname(__file__)        
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
    
    file_path = os.path.join(project_root, '..', 'data_raw', 'credit_refunded.csv')
    return pd.read_csv(file_path)

def preprocess_df_refunds():
    df_refunds = load_csv_credits_refunds()

    # Convert the date column to a datetime format
    df_refunds['date'] = pd.to_datetime(df_refunds['Accounting Date'], format = '%m/%d/%Y')
    df_refunds.drop(columns = 'Accounting Date', inplace = True)

    # Rename columns to match the sql table
    df_refunds.rename(columns={"masked_column": "credit_refunded", "Item Payment Type": "payment_type"}, inplace = True)

    return df_refunds

