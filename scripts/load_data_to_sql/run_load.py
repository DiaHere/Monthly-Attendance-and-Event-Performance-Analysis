from preprocess_raw_data.load_attendance import load_csv_attendance
from universal_loader import load_data_to_sql

def main():
    # attendance performance data loading
    df_attendance = load_csv_attendance()
    attendance_columns = df_attendance.columns

    load_data_to_sql(df_attendance, 'attendance', attendance_columns, 'month_year')



if __name__ == '__main__':
    main()