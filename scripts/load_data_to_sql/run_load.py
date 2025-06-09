from preprocess_raw_data.preprocess_attendance import preprocess_df_attendance
from preprocess_raw_data.preprocess_events import preprocess_df_events
from preprocess_raw_data.preprocess_post_event_surverys import preprocess_df_post_event_sur
from preprocess_raw_data.preprocess_donations import preprocess_df_donations
from preprocess_raw_data.preprocess_credits_refunded import preprocess_df_refunds
from preprocess_raw_data.preprocess_tickets import preprocess_df_tickets


from universal_loader import load_data_to_sql

import warnings
warnings.filterwarnings('ignore') # Ignores all warnings
warnings.filterwarnings('ignore', category=DeprecationWarning) # Ignores only DeprecationWarnings

def main():
    # the preprocessed and cleaned attendance performance data 
    df_attendance = preprocess_df_attendance()
    attendance_col = df_attendance.columns
    # loading the ready data into the sql database to the correct table and primary key
    load_data_to_sql(df_attendance, 'attendance', attendance_col, 'month_year')

    # the preprocessed and cleaned events data 
    df_events = preprocess_df_events()
    envets_col = df_events.columns
    # loading the ready data into the sql database to the correct table and primary key
    load_data_to_sql(df_events, 'events', envets_col, 'event_title')

    df_surveys = preprocess_df_post_event_sur()
    surveys_col = df_surveys.columns
    load_data_to_sql(df_surveys, 'post_event_surveys', surveys_col, 'event_title')
    
    df_donations = preprocess_df_donations()
    donations_col = df_donations.columns
    load_data_to_sql(df_donations, 'donations', donations_col, 'date')

    df_refunds = preprocess_df_refunds()
    refunds_col = df_refunds.columns
    load_data_to_sql(df_refunds, 'credit_refunds', refunds_col, 'date')

    df_tickets = preprocess_df_tickets()
    tickets_col = df_tickets.columns
    load_data_to_sql(df_tickets, 'tickets', tickets_col, 'date')
    
if __name__ == '__main__':
    main()