-- post event surveys

-- add the event_id reference from events table
UPDATE post_event_surveys AS surveys
JOIN events AS e
    ON surveys.event_title = e.event_title
SET surveys.event_id = e.event_id;

UPDATE post_event_surveys
SET date = NULL
WHERE date IN ("0001-01-01");

UPDATE post_event_surveys AS s
JOIN events AS e
    ON s.event_title = e.event_title
SET s.date = e.date
WHERE s.date IS NULL;

-- attendance 

-- attendance inforamtion per year
SELECT
    SUM(total_attendance) AS total_attendance, 
    SUM(total_first_time_visitors) AS first_time_visitors, 
    YEAR(month_year) AS year
FROM attendance
GROUP BY year;

-- attendance inforamtion based on the month of the year, excluding the months of 2025 due to only the first two months recorded only
SELECT
    SUM(total_attendance) AS total_attendance, 
    SUM(total_first_time_visitors) AS first_time_visitors, 
    MONTH(month_year) AS month
FROM attendance
WHERE month_year < '2025-01-01'
GROUP BY month;

-- Income Group Attendance
SELECT 
    annual_household_income,
    COUNT(*) AS num_attendees
FROM post_event_surveys
GROUP BY annual_household_income
ORDER BY num_attendees DESC;

-- First time visiors ratio 
SELECT 
    month_year,
    ROUND(total_first_time_visitors / total_attendance, 2) AS first_timer_ratio
FROM attendance
WHERE total_attendance > 0;

-- events + attendace

-- Grouping Attendances with Events
SELECT calendar_date,
    e.event_title AS title,
    a.total_attendance AS total_monthly_attendance,
    ROUND((e.end_time - e.start_time) / 100, 2) AS duration,
    a.total_first_time_visitors AS monthly_first_time_visitors
FROM dim_calendar AS  c
LEFT JOIN events AS e ON date = calendar_date
LEFT JOIN attendance AS a ON month_year = calendar_date
WHERE e.event_id IS NOT NULL 
    OR a.total_attendance IS NOT NULL;


-- Which events led to higher attendance and first time visitors rate?
SELECT 
    e.date AS event_date,
    e.event_title,
    ROUND((e.end_time - e.start_time) / 100, 2) AS duration,
    monthly_event_counts.num_events,
    ROUND(a.total_attendance / monthly_event_counts.num_events, 2) AS avg_attendance_per_event
FROM events AS e
LEFT JOIN attendance AS a 
    ON MONTH(e.date) = MONTH(a.month_year) AND YEAR(e.date) = YEAR(a.month_year)
LEFT JOIN (
    SELECT 
        MONTH(date) AS month,
        YEAR(date) AS year,
        COUNT(*) AS num_events
    FROM events
    GROUP BY YEAR(date), MONTH(date)
) AS monthly_event_counts
    ON MONTH(e.date) = monthly_event_counts.month
    AND YEAR(e.date) = monthly_event_counts.year
ORDER BY event_date;

-- Transactions

-- donations per month
SELECT 
    DATE_FORMAT(date, '%Y-%m') AS month_year,
    ROUND(SUM(donation_received) / 1000, 2) AS donations_by_thousands
FROM donations
GROUP BY month_year
ORDER BY month_year;


-- tickets sales per event
SELECT 
    event_title,
    SUM(ticket_prices) AS tickets_sales, 
    COUNT(event_title) AS num_tickets_sold
FROM tickets
GROUP BY event_title
ORDER BY tickets_sales;

-- tickets sales per month 
SELECT 
    DATE_FORMAT(date, '%Y-%m') AS month_year,
    ROUND(SUM(ticket_prices / 1000),2) AS tickets_sales_by_thousands,
    COUNT(ticket_prices) AS num_tickets_sold
FROM tickets
GROUP BY month_year
ORDER BY month_year;

-- tickets and attendances
SELECT 
    DATE_FORMAT(t.date, '%Y-%m') AS month_year,
    SUM(t.ticket_prices) AS ticket_sales,
    COUNT(t.ticket_prices) AS num_tickets_sold,
    a.total_attendance
FROM tickets AS t
JOIN attendance AS a ON DATE_FORMAT(t.date, '%Y-%m') = DATE_FORMAT(a.month_year, '%Y-%m')
GROUP BY DATE_FORMAT(t.date, '%Y-%m'), a.total_attendance
ORDER BY month_year;


-- total gain/loss per month 
SELECT 
    month_year,
    SUM(ticket_total + donation_total + refund_total) AS total_net
FROM (
    SELECT 
        DATE_FORMAT(date, '%Y-%m') AS month_year,
        SUM(ticket_prices) AS ticket_total,
        0 AS donation_total,
        0 AS refund_total
    FROM tickets
    GROUP BY month_year

    UNION ALL

    SELECT 
        DATE_FORMAT(date, '%Y-%m') AS month_year,
        0 AS ticket_total,
        SUM(donation_received) AS donation_total,
        0 AS refund_total
    FROM donations
    GROUP BY month_year

    UNION ALL

    SELECT 
        DATE_FORMAT(date, '%Y-%m') AS month_year,
        0 AS ticket_total,
        0 AS donation_total,
        SUM(credit_refunded) AS refund_total
    FROM credit_refunds
    GROUP BY month_year
) AS monthly_data
GROUP BY month_year
ORDER BY month_year;

-- coorelation between gains and monthly attendance
SELECT 
    monthly_net_sales.month_year,
    SUM(monthly_net_sales.ticket_total + monthly_net_sales.donation_total + monthly_net_sales.refund_total) AS total_net,
    attendance.total_attendance
FROM (
    SELECT 
        DATE_FORMAT(date, '%Y-%m') AS month_year,
        SUM(ticket_prices) AS ticket_total,
        0 AS donation_total,
        0 AS refund_total
    FROM tickets
    GROUP BY month_year

    UNION ALL

    SELECT 
        DATE_FORMAT(date, '%Y-%m') AS month_year,
        0 AS ticket_total,
        SUM(donation_received) AS donation_total,
        0 AS refund_total
    FROM donations
    GROUP BY month_year

    UNION ALL

    SELECT 
        DATE_FORMAT(date, '%Y-%m') AS month_year,
        0 AS ticket_total,
        0 AS donation_total,
        SUM(credit_refunded) AS refund_total
    FROM credit_refunds
    GROUP BY month_year
) AS monthly_net_sales
JOIN attendance 
    ON DATE_FORMAT(attendance.month_year, '%Y-%m') = monthly_net_sales.month_year
GROUP BY monthly_net_sales.month_year, attendance.total_attendance
ORDER BY monthly_net_sales.month_year;
