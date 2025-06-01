-- Create the database if it does not already exist and switch to it.
CREATE DATABASE IF NOT EXISTS theatre_performance_data;
USE theatre_performance_data;

-- Create attendance table
CREATE TABLE IF NOT EXISTS attendance(
    month_year DATE PRIMARY KEY,
    total_days_in_use INT,
    num_sep_events INT,
    total_unique_patrons INT,
    total_attendance INT,
    total_first_time_visitors INT
);

-- View the attendance table
SELECT *
FROM attendance;


-- Create events table
CREATE TABLE IF NOT EXISTS events(
    event_title VARCHAR(100) PRIMARY KEY,
    date DATE,
    start_time INT,
    end_time INT
);

-- View the events table
SELECT *
FROM events;

-- Create post event survey responses table
CREATE TABLE IF NOT EXISTS post_event_surveys(
    event_title VARCHAR(100),
    id INT PRIMARY KEY,
    date DATE,
    source_of_hearing TEXT,
    age_group VARCHAR(15),
    annual_household_income VARCHAR(20),
    overal_event_expression TEXT,
    feeback_suggestion TEXT
);

-- View post_event_surveys
SELECT *
FROM post_event_surveys;


-- Create donations table
CREATE TABLE IF NOT EXISTS donations(
    date_range DATE,
    donation_received INT
);

ALTER TABLE donations
MODIFY date_range DATE,
DROP PRIMARY KEY;

-- View donations
SELECT *
FROM donations;

-- Create Credit Refunds table
CREATE TABLE IF NOT EXISTS credit_refunds(
    date_range DATE,
    credit_refunded INT,
    payment_type VARCHAR(20)
);

-- View credit_refunds
SELECT *
FROM credit_refunds;

-- Create tickets table
CREATE TABLE IF NOT EXISTS tickets(
    date_range DATE,
    event_title VARCHAR(100),
    payment_type VARCHAR(20),
    ticket_prices INT
);

-- View tickets
SELECT *
FROM tickets;


-- View all TABLES
SHOW TABLES;
