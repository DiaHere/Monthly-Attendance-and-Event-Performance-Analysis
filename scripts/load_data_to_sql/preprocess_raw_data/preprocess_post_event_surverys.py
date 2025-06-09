import pandas as pd 
from datetime import datetime
import os

# Load the CSV
# post event surveys data
def load_csv_post_event_sur():
    current_dir = os.path.dirname(__file__)        
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
    
    file_path = os.path.join(project_root, '..', 'data_raw', 'post_events_survey_data_combined.csv')
    return pd.read_csv(file_path)

def preprocess_df_post_event_sur():
    df_surveys = load_csv_post_event_sur()

    # Combine all the columns of source of hearing into one
        # List of all "source of hearing" columns to consolidate into a single column
    source_of_hearing = ['Walla Walla Union Bulletin', 'Tri-City Herald',
       'The East Oregonian', 'The Entertainer', 'Tumbleweird', 'Radio',
       'Poster', 'Social Media (Facebook, Twitter, Instagram)', 'Email',
       'Word of Mouth', 'Gesa Power House Theatre website (www.phtww.org)','Other'] # df_surveys[col].replace('Yes', col) for col in source_of_hearing if row[col] == 

        # Create a new column 'source_of_hearing' as a list of sources selected in each row
    df_surveys['source_of_hearing'] = df_surveys[source_of_hearing].apply(
        lambda raw: [col if raw[col] == 'Yes' else raw[col] for col in source_of_hearing], 
        axis = 1)
    
        # Remove 'No' and null values from the 'source_of_hearing' lists to only keep actual sources
    df_surveys['source_of_hearing'] = df_surveys['source_of_hearing'].apply(
        lambda sources: [i for i in sources if i != 'No' and pd.notnull(i)]
        )
        # Convert each list to string 
    df_surveys['source_of_hearing'] = df_surveys['source_of_hearing'].apply(lambda x: ', '.join(x))

    # Drop the original source of hearing columns as they're now redundant
    df_surveys.drop(columns = source_of_hearing, inplace = True)


    # Combine the 'event' and 'Event' columns into a single 'event_title' column, prioritizing non-null values
    df_surveys['event_title'] = df_surveys['event'].combine_first(df_surveys['Event'])
    df_surveys = df_surveys.dropna(subset = ['event_title']).reset_index(drop = True)

    # Create a date column with datetime formate of each event time
    # there are lots of missing values, eahc event will be matched with the correct date from the events table
    df_surveys['date'] = pd.to_datetime(df_surveys['Instance'], format='%m/%d/%Y')

    # Remove columns that are no longer needed after consolidation and cleaning
    df_surveys.drop(columns = ['event','Television','Event','Instance','The Idaho Statesman','ParentMap','Date', 'ID'], inplace = True)

    # Rename columns to match the sql table
    df_surveys.rename(columns={
    "What is your age group?": "age_group",
    "What is your annual household income?": "annual_household_income",
    "What was your overall impression of this event (quality, lighting, sound, value)?": "overal_event_expression",
    "Please share any other suggestions or ideas that would help us enhance your experience at Gesa Power House Theatre. If you would like someone to respond to your feedback, please include your contact information. Thank you!": "feeback_suggestion",
    }, inplace = True)


    # replace all nan values with None, which is acceptable in sql unlike nan 
    df_surveys = df_surveys.where(pd.notnull(df_surveys), None)
    df_surveys['date'] = df_surveys['date'].where(pd.notnull(df_surveys['date']), None)

    return df_surveys