import pandas as pd 
from datetime import datetime
import os

# Load the CSV
# donations data
def load_csv_donations_csv():
    current_dir = os.path.dirname(__file__)        
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
    
    file_path = os.path.join(project_root, '..', 'data_raw', 'post_events_survey_data_combined.csv')
    return pd.read_csv(file_path)

def preprocess_df_donations():
    df_donations = load_csv_donations_csv()

    return df_donations
