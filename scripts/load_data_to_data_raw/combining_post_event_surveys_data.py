import os
import glob
import re
import pandas as pd

def post_event_survey_responses(folder_path):
    """Read all survey CSV files and return a combined DataFrame."""
    
    files = glob.glob(os.path.join(folder_path, "*.csv"))
    pattern = r'PostShowSurvey\d+\d{4}(.+?)(\d*)\.csv$'
    df_list = []
    
    for file in files:
        df = pd.read_csv(file)
        filename = os.path.basename(file)
        match = re.search(pattern, filename)
        if match:
            event_name = match.group(1)
            df['event'] = event_name
        df_list.append(df)

    # Combine all DataFrames into one.
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df

def export_to_csv(data, filename="output.csv"):
    """Export the given DataFrame to CSV."""

    if isinstance(data, pd.DataFrame):
        data.to_csv(filename, index=False, encoding="utf-8")
        print(f"Data exported to CSV at '{filename}'.")
    else:
        print("Data type not supported for CSV export.")


def main():
    """Combine all post-event survey responses into a single CSV if needed."""

    script_dir   = os.path.dirname(__file__) 
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    survey_folder = os.path.join(project_root, "data_raw")
    output_csv_path = os.path.join(project_root, "data_raw", "post_events_survey_data_combined.csv")

    if os.path.exists(output_csv_path):
        print("post_events_survey_data_combined.csv already exists. Skipping export.")
    else:
        print("post_events_survey_data_combined.csv not found. Processing survey responses...")
        survey_df = post_event_survey_responses(survey_folder)
        export_to_csv(survey_df, filename=output_csv_path)
        print("Exported survey data to post_events_survey_data_combined.csv")


if __name__ == '__main__':
    main()

