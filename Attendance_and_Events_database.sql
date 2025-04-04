-- Create the database if it does not already exist and switch to it.
CREATE DATABASE IF NOT EXISTS theatre_performance_data;
USE theatre_performance_data;

-- Create attendance table with the appropriate columns 
CREATE TABLE IF NOT EXISTS attendance(
    month_year DATE PRIMARY KEY,
    total_days_in_use INT,
    num_sep_events INT,
    total_unique_patrons INT,
    total_attendance INT,
    total_first_time_visitors INT
);


-- Start a transaction to ensure atomicity during data load.
START TRANSACTION;

-- Load data from the CSV file.
-- Note:
-- 1. The CSV file contains month/year in the format "MM/YY".
-- 2. We append '/01' to create a full date (e.g., "01/23" becomes "01/23/01" meaning January 1, 2023).
-- 3. Adjust the file path as necessary.
-- 4. The data has been modified for confidentiality purposes; however, its scale remains unchanged

-- Ensure to put the correct file path
LOAD DATA INFILE '/Users/diadana/Desktop/ComputerScience/Monthly-Attendance-and-Event-Performance-Analysis/attendance_performance_data.csv'
INTO TABLE attendance
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@month_year,num_sep_events, total_days_in_use, total_unique_patrons, total_attendance, total_first_time_visitors)
SET month_year = STR_TO_DATE(CONCAT(@month_year, '/01'), '%m/%y/%d');

-- If the load is successful, commit the transaction.
COMMIT;

SELECT *
FROM attendance;