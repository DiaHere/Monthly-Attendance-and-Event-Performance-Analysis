import pandas as pd 
import os

# Load the CSV
# Attendance Performance data
def load_csv_attendance():
    current_dir = os.path.dirname(__file__)        
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
    
    file_path = os.path.join(project_root, '..', 'data_raw', 'attendance_performance_data.csv')
    df_attendance = pd.read_csv(file_path)

    # Clean the data
    # Change the date column to a date format
    df_attendance['month_year'] = pd.to_datetime(df_attendance['date'], format='%m/%y')

    # rename the columns of the dataframe to match the sql table
    df_attendance.rename(columns={
    "Total days in use": "total_days_in_use",
    "Number of separate events": "num_sep_events",
    "Total unique patrons": "total_unique_patrons",
    "Total attendance": "total_attendance",
    "First time visitors": "total_first_time_visitors"
    }, inplace = True)

    # return the dataframe
    return df_attendance
    

