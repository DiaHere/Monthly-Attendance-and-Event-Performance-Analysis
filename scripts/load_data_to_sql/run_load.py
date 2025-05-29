from load_attendance import load_csv, insert_attendance_data

def main():
    df = load_csv()
    insert_attendance_data(df)

if __name__ == '__main__':
    main()