import pandas as pd 
from datetime import datetime
import os

# Load the CSV
# Events data
def load_csv_events():
    current_dir = os.path.dirname(__file__)        
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
    
    file_path = os.path.join(project_root, '..', 'data_raw', 'events_data.csv')
    return pd.read_csv(file_path)

def time_str_to_int(x):
    if x == 0 or pd.isna(x):
        return 0
    # parse "9:30 AM" or "6:30 PM" to datetime
    t = datetime.strptime(x, "%I:%M %p")
    return t.hour * 100 + t.minute

def preprocess_df_events():
    df_events = load_csv_events()

    # clean the data
    # convert date column type to datetime
    df_events['date'] = pd.to_datetime(df_events['date'], format='%Y-%m-%d')

    # convert title column type to string
    df_events['title'] = df_events['title'].astype(str)

    # change null calues of those two columns to zero
    df_events['start'].fillna(0, inplace = True)
    df_events['end'].fillna(0, inplace = True)

    # convert from 12-hour clock time to 24-hour time
    df_events['start'] = df_events['start'].apply(time_str_to_int) 
    df_events['end'] = df_events['end'].apply(time_str_to_int) 

    # Rename columns to match the sql table
    df_events.rename(columns={
    "title": "event_title",
    "start": "start_time",
    "end": "end_time",
    }, inplace = True)

# Handle duplicates by adding a note next to the reoccured event in paraenthesis
    df_events['event_title'] = (
        df_events.groupby('event_title').cumcount()
        .replace(0, '')
        .astype(str)
        .radd(df_events['event_title'])
        .replace(r'(.+?)([1-9]+)$', r'\1(\2)', regex=True)
    )

    return df_events

