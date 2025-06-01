from preprocess_raw_data.preprocess_attendance import preprocess_df_attendance
from preprocess_raw_data.preprocess_events import preprocess_df_events
from preprocess_raw_data.preprocess_post_event_surverys import preprocess_df_post_event_sur
from preprocess_raw_data.preprocess_donations import preprocess_df_donations


from universal_loader import load_data_to_sql

import warnings
warnings.filterwarnings('ignore') # Ignores all warnings
warnings.filterwarnings('ignore', category=DeprecationWarning) # Ignores only DeprecationWarnings

def main():
    # attendance performance data loading
    df_attendance = preprocess_df_attendance()
    attendance_col = df_attendance.columns
    load_data_to_sql(df_attendance, 'attendance', attendance_col, 'month_year')

    df_events = preprocess_df_events()
    envets_col = df_events.columns
    load_data_to_sql(df_events, 'events', envets_col, 'event_title')

    df_surveys = preprocess_df_post_event_sur()
    surveys_col = df_surveys.columns
    load_data_to_sql(df_surveys, 'post_event_surveys', surveys_col, 'event_title')

    df_donations = preprocess_df_donations()
    print(df_donations)


if __name__ == '__main__':
    main()