import requests
from bs4 import BeautifulSoup

import os
import csv

def scrab_all_year_data():
    """Scrape event data from the theatre website between 2023 and Feb 2025."""
    recent_titles = [] 
    events_title_time_list = []

    for year in range(2023, 2026):
        for month in range(1, 13):
            if year == 2025 and month == 3:
                break

            url = f'https://phtww.org/shows/month/{year}-{month:02d}/'
            response = requests.get(url)
            
            if response.status_code != 200:
                print(f"Failed to fetch {url}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 1. Extract all event title <a> tags.
            event_tags = soup.find_all(
                'a', 
                class_="tribe-events-calendar-month-mobile-events__mobile-event-title-link tribe-common-anchor"
            )
            
            # 2. Extract all <time> tags that represent times with HH:MM datetime format.
            time_tags = soup.find_all('time', attrs={'datetime': lambda dt: dt and len(dt) == 5})
            # Group time tags into pairs (start, end) in the order they appear.
            time_pairs = list(zip(time_tags[::2], time_tags[1::2]))
            
            # 3. Iterate over event tags and assign the corresponding time pair by index.
            for idx, tag in enumerate(event_tags):
                title = tag.get_text(strip=True)
                if title != "Private Event" and title not in recent_titles:
                    # Update sliding window: add current title and remove the oldest if needed.
                    recent_titles.append(title)
                    if len(recent_titles) > 3:
                        recent_titles.pop(0)
                
                    # Retrieve the event date from the previous <time> tag (ideally with a full date).
                    date_tag = tag.find_previous('time')
                    date = date_tag['datetime'] if date_tag else "Unknown"
                    
                    # Get the corresponding time pair (start, end) using the index (if available).
                    if idx < len(time_pairs):
                        start_time = time_pairs[idx][0].get_text(strip=True)
                        end_time = time_pairs[idx][1].get_text(strip=True)
                    else:
                        start_time, end_time = None, None

                    # Append the event info as a dictionary.
                    events_title_time_list.append({
                        "title": title,
                        "date": date,
                        "start": start_time,
                        "end": end_time
                    })
                    
    return events_title_time_list

def export_to_csv(data, filename="output.csv"):
    """Export the given data to a CSV file using the csv module."""

    if isinstance(data, list):
        if not data:
            print("No data to export.")
            return
        
        # Extract headers from the keys of the first dictionary.
        headers = list(data[0].keys())
        with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for row in data:
                writer.writerow(row)

def main():
    """Download event data if it doesn't already exist."""

    base_dir = os.path.dirname(os.path.dirname(__file__))
    project_root = os.path.dirname(base_dir)

    # Build the absolute paths for the input folder and output CSV inside data_raw.
    output_csv_path = os.path.join(project_root, "data_raw")
    
    # Export scraped event data.
    if os.path.exists(output_csv_path):
        print('"events_data.csv" already exists. Skipping download.')
    else:
        events = scrab_all_year_data()
        export_to_csv(events, filename=output_csv_path)
        print("Exported event data to 'events_data.csv'.")
    
if __name__ == '__main__':
    main()
