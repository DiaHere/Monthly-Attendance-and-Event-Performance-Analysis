import os
import glob
import re
import pandas as pd

def post_event_survey_responses(folder_path):
    """
    Processes CSV files in a specified folder containing post-event survey responses,
    extracts the event name from the file names, and concatenates all responses into
    a single pandas DataFrame.
    
    The filename pattern is expected to match:
        PostShowSurvey{surveyNumber}{year}{eventName}{optionalTrailingDigits}.csv

    Args:
        folder_path (str): Absolute or relative path to the folder containing the CSV files.

    Returns:
        DataFrame: A pandas DataFrame with all survey responses and an added column 
                   "event" containing the extracted event name.
    """
    files = glob.glob(os.path.join(folder_path, "*.csv"))
    pattern = r'PostShowSurvey\d+\d{4}(.+?)(\d*)\.csv$'
    df_list = []
    
    for file in files:
        # Read each file into a DataFrame.
        df = pd.read_csv(file)
        # Use only the filename (not the full path) for pattern matching.
        filename = os.path.basename(file)
        match = re.search(pattern, filename)
        if match:
            event_name = match.group(1)
            # Add the extracted event name as a new column.
            df['event'] = event_name
        df_list.append(df)

    # Combine all DataFrames into one.
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df


def export_to_csv(data, filename="output.csv"):
    """
    Exports the given data to a CSV file. 
    If the data is a pandas DataFrame, it utilizes the DataFrame's to_csv() method.
    
    Args:
        data: The data to export. Should be a DataFrame.
        filename (str): The target CSV file path.
    """
    if isinstance(data, pd.DataFrame):
        data.to_csv(filename, index=False, encoding="utf-8")
        print(f"Data exported to CSV at '{filename}'.")
    else:
        print("Data type not supported for CSV export.")


def main():
    """
    Main function that:
      - Checks if the 'post_events_survey_data.csv' already exists in the data_raw folder.
      - If not, processes survey responses from 'data_raw/Post-Event-Survey-Responses'
        and exports them to 'data_raw/post_events_survey_data.csv'.
    
    Assumes a project structure like:
    
    project_root/
      data_raw/
        Post-Event-Survey-Responses/   (folder containing CSV files)
        post_events_survey_data.csv     (combined output)
      scripts/
        my_script.py   (this script)
    """
    # Determine the base directory of the project.
    # Since this script is in the 'scripts' folder, go one level up.
    base_dir = os.path.dirname(os.path.dirname(__file__))
    
    # Build the absolute paths for the input folder and output CSV inside data_raw.
    survey_folder = os.path.join(base_dir, "data_raw", "Post-Event-Survey-Responses")
    output_csv_path = os.path.join(base_dir, "data_raw", "post_events_survey_data.csv")

    # Check if the combined survey CSV already exists.
    if os.path.exists(output_csv_path):
        print("post_events_survey_data.csv already exists. Skipping export.")
    else:
        print("post_events_survey_data.csv not found. Processing survey responses...")
        survey_df = post_event_survey_responses(survey_folder)
        export_to_csv(survey_df, filename=output_csv_path)
        print("Exported survey data to post_events_survey_data.csv")


if __name__ == '__main__':
    main()
