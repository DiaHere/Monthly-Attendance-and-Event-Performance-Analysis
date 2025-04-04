CREATE DATABASE IF NOT EXISTS theatre_performance_data;

CREATE TABLE attendance(
    month_year TIMESTAMP PRIMARY KEY,
    total_days_in_use INT,
    total_unique_patrons INT,
    total_attendance INT,
    total_first_time_visitors INT
);


SELECT *
FROM attendance;

ALTER TABLE attendance MODIFY COLUMN month_year DATE; -- match the csv file's data column to have a smoother uploading process

LOAD DATA INFILE '/Users/diadana/Desktop/ComputerScience/Monthly-Attendance-and-Event-Performance-Analysis/attendance_performace_data.csv'
INTO TABLE attendance
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@month_year, total_days_in_use, total_unique_patrons, total_attendance, total_first_time_visitors)
SET month_year = STR_TO_DATE(@month_year, '%m/$y');


SELECT *
FROM attendance;

