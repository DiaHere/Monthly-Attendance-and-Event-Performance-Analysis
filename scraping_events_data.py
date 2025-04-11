import requests
from bs4 import BeautifulSoup
import csv
import os
import pandas as pd
import glob
import re

def scrab_all_year_data():
    """
    Scrapes event data from the Gesa Power House Theatre website for events between 2023 and Feb 2025.
    
    This function iterates through each month within the given year range, sends HTTP GET 
    requests to the monthly events pages, and uses BeautifulSoup to extract event titles, dates, 
    and times. A sliding window of the last three event titles is maintained to avoid duplicate entries.
    
    Returns:
        list: A list of dictionaries, each containing the following keys:
            - "title": The event title.
            - "date": The event date as found on the page.
            - "start": The start time (from the first time tag in a time pair).
            - "end": The end time (from the second time tag in a time pair).
    """
    recent_titles = []            # Sliding window for the last 3 event titles to avoid duplicates.
    events_title_time_list = []   # List to store event dictionaries.

    for year in range(2023, 2026):
        for month in range(1, 13):
            # Stop processing after February 2025.
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


def post_event_survey_responses(folder_path):
    """
    Processes CSV files in a specified folder containing post-event survey responses,
    extracts the event name from the file names, and concatenates all responses into
    a single pandas DataFrame.
    
    The filename pattern is expected to match:
        PostShowSurvey{surveyNumber}{year}{eventName}{optionalTrailingDigits}.csv

    Args:
        folder_path (str): Relative path to the folder containing the CSV files.

    Returns:
        DataFrame: A pandas DataFrame with all survey responses and an added column 
                   "event" containing the extracted event name.
    """
    # Build the data directory using a path relative to this file.
    data_dir = os.path.join(os.path.dirname(__file__), folder_path)
    files = glob.glob(os.path.join(data_dir, "*.csv"))
    
    pattern = r'PostShowSurvey\d+\d{4}(.+?)(\d*)\.csv$'
    df_list = []
    
    for file in files:
        # Read each file into a DataFrame.
        df = pd.read_csv(file)

        # Extract event name from the filename (use basename to remove directory info).
        filename = os.path.basename(file)
        match = re.search(pattern, filename)
        if match:
            event_name = match.group(1)
            # Create a new column "event" in the DataFrame.
            df['event'] = event_name
        df_list.append(df)

    # Combine all DataFrames into one.
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df
    

def export_to_csv(data, filename="output.csv"):
    """
    Exports the given data to a CSV file. If the data is a list of dictionaries,
    it uses the csv module. If the data is a pandas DataFrame, it utilizes the 
    DataFrame's to_csv() method.
    
    Args:
        data: The data to export; can be either a list of dictionaries or a DataFrame.
        filename (str): The target CSV file name.
    """
    if isinstance(data, list):
        # Assume list of dictionaries.
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
    elif isinstance(data, pd.DataFrame):
        data.to_csv(filename, index=False, encoding="utf-8")
    else:
        print("Data type not supported for CSV export.")
    

def main():
    """
    Main function that:
        1. Checks if 'events_data.csv' exists. If not, scrapes event data and exports it.
        2. Checks if 'post_events_survey_data.csv' exists. If not, processes survey responses and exports them.
    """
    # Export scraped event data.
    if os.path.exists('events_data.csv'):
        print('"events_data.csv" already exists. Skipping download.')
    else:
        events = scrab_all_year_data()
        export_to_csv(events, filename="events_data.csv")
        print("Exported event data to 'events_data.csv'.")

    # Export post-event survey responses.
    if os.path.exists('post_events_survey_data.csv'):
        print('"post_events_survey_data.csv" already exists. Skipping download.')
    else:
        survey = post_event_survey_responses('Post-Event-Survey-Responses')
        export_to_csv(survey, filename="post_events_survey_data.csv")
        print("Exported survey data to 'post_events_survey_data.csv'.")
    

if __name__ == '__main__':
    main()
