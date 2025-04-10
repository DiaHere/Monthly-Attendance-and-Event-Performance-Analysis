import requests
from bs4 import BeautifulSoup
import csv
import os

def scrab_all_year_data():
    """
    Scrapes event data from the Gesa Power House Theatre website for events between 2023 and Feb 2025.
    
    This function iterates through each month within the given year range, sends HTTP GET 
    requests to the monthly events pages, and uses BeautifulSoup to extract event titles, dates, 
    and times. A sliding window of the last three event titles is maintained to avoid 
    duplicate entries.
    
    Returns:
        list: A list of dictionaries, each containing the following keys:
              - "title": The event title.
              - "date": The event date as found in the page.
              - "start": The start time (from the first time tag in a time pair).
              - "end": The end time (from the second time tag in a time pair).
    """
    recent_titles = []            # Sliding window for the last 3 event titles to avoid duplicates.
    events_title_time_list = []   # List to store event dictionaries.

    for year in range(2023, 2026):
        for month in range(1, 13):
            # Stop processing after February 2025
            if year == 2025 and month == 3:
                break

            url = f'https://phtww.org/shows/month/{year}-{month:02d}/'
            response = requests.get(url)
            
            if response.status_code != 200:
                print(f"Failed to fetch {url}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 1. Extract all event title <a> tags.
            event_tags = soup.find_all('a', 
                                       class_="tribe-events-calendar-month-mobile-events__mobile-event-title-link tribe-common-anchor")
            
            # 2. Extract all <time> tags that represent times (with HH:MM datetime format).
            time_tags = soup.find_all('time', attrs={'datetime': lambda dt: dt and len(dt) == 5})
            # Group time tags into pairs (start, end) based on their order.
            time_pairs = list(zip(time_tags[::2], time_tags[1::2]))
            
            # 3. Iterate over event tags and assign the corresponding time pair by index.
            for idx, tag in enumerate(event_tags):
                title = tag.get_text(strip=True)
                if title != "Private Event" and title not in recent_titles:
                    # Update sliding window: add current title and remove the oldest if needed.
                    recent_titles.append(title)
                    if len(recent_titles) > 3:
                        recent_titles.pop(0)
                
                    # Retrieve the event date from the previous <time> tag (ideally containing the full date).
                    date_tag = tag.find_previous('time')
                    date = date_tag['datetime'] if date_tag else "Unknown"
                    
                    # Get the corresponding time pair (start, end) using the index.
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


def export_to_csv(events, filename="events_data.csv"):
    """
    Exports a list of event dictionaries to a CSV file.
    
    Args:
        events (list): List of dictionaries containing event data.
        filename (str): The name of the CSV file to write.
    """
    # Define the CSV header based on keys in the event dictionaries
    headers = ["title", "date", "start", "end"]
    
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for event in events:
            writer.writerow(event)


def main():
    """
    Main function that scrapes the event data and exports the data as a csv file, if the file doesn't exsit yet.
    """
    if os.path.exists('events_data.csv'):
        print('"events_data.csv" already exists. Skipping download.')
    else: 
        events = scrab_all_year_data()
        export_to_csv(events)

if __name__ == '__main__':
    main()
