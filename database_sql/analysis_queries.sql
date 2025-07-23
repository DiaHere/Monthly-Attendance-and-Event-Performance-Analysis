-- filling in the null date values in post_event_surveys

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


-- monthly averge attendance per event
ALTER TABLE attendance
ADD COLUMN attendance_per_event FLOAT;

UPDATE attendance
SET attendance_per_event = total_attendance/num_sep_events;

-- attendance inforamtion per year
SELECT ROUND(SUM(attendance_per_event)) AS avg_attendance_per_event, 
    SUM(total_attendance) AS total_attendance, 
    SUM(total_first_time_visitors) AS first_time_visitors, 
    YEAR(month_year) AS year
FROM attendance
GROUP BY year;

-- attendance inforamtion based on the month of the year
SELECT ROUND(SUM(attendance_per_event)) AS avg_attendance_per_event,
    SUM(total_attendance) AS total_attendance, 
    SUM(total_first_time_visitors) AS first_time_visitors, 
    MONTH(month_year) AS month
FROM attendance
GROUP BY month;


SELECT calendar_date,
    e.event_id AS id,
    e.event_title AS title,
    a.total_attendance AS total_monthly_attendance,
    a.attendance_per_event AS average_attendance_per_event,
    ROUND((e.end_time - e.start_time) / 100, 2) AS duration,
    a.total_first_time_visitors AS monthly_first_time_visitors
FROM dim_calendar AS  c
LEFT JOIN events AS e ON date = calendar_date
LEFT JOIN attendance AS a ON month_year = calendar_date
WHERE e.event_id IS NOT NULL 
    OR a.total_attendance IS NOT NULL;