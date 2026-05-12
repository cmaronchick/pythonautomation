import os
import json
import gspread
from jira import JIRA
import pandas as pd
from datetime import datetime
# import config

# --- Configuration ---
JIRA_SERVER = 'https://2kcatd.atlassian.net/'
JIRA_EMAIL = 'christopher.aronchick@catdaddy.com'
JIRA_API_TOKEN = os.environ['JIRA_API_TOKEN']
FIX_VERSION = 'S8 Update 4'
STORY_POINTS_FIELD = 'customfield_10026' 
GOOGLE_SHEET_ID = '1uwAg2ohnYHb_bwdZXDsEG_kkytT0lLQzsU6TIuxEsCU' # Paste your ID here
SHEET_TAB_NAME = 'Sheet1' # Change if your tab is named differently

# The custom field ID for Story Points varies by Jira instance.
# You can find yours by looking at the JSON of a single issue via the API.
STORY_POINTS_FIELD = 'customfield_10026' 
today = datetime.now().strftime('%Y-%m-%d')
estimatedStories = 0

def get_jira_client():
    return JIRA(
        server=JIRA_SERVER,
        basic_auth=(os.environ['JIRA_EMAIL'], os.environ['JIRA_API_TOKEN'])
    )

def fetch_daily_sprint_data(jira):
    jql_query = f'fixVersion = "{FIX_VERSION}" AND issueType in (Story, Task, Bug)'
    issues = jira.search_issues(jql_query, maxResults=False)
    
    data = []
    today = datetime.now().strftime('%Y-%m-%d')

    for issue in issues:
        story_points = getattr(issue.fields, STORY_POINTS_FIELD, 0)
        epic_key = issue.fields.parent.key if hasattr(issue.fields, 'parent') else "No Epic"

        data.append([
            today,
            issue.key,
            epic_key,
            issue.fields.summary,
            issue.fields.status.name,
            story_points if story_points is not None else 0
        ])
    return data

def upsert_to_google_sheet(daily_data):
    # 1. Authenticate with Google
    creds_json = os.environ['GOOGLE_CREDENTIALS']
    creds_dict = json.loads(creds_json)
    gc = gspread.service_account_from_dict(creds_dict)
    
    sh = gc.open_by_key(GOOGLE_SHEET_ID)
    worksheet = sh.worksheet(SHEET_TAB_NAME)
    
    # 2. Fetch existing data from the sheet
    existing_data = worksheet.get_all_records()
    df_existing = pd.DataFrame(existing_data)
    
    # 3. Convert today's new Jira pull into a DataFrame
    columns = ['Date', 'Issue Key', 'Epic', 'Summary', 'Status', 'Story Points']
    df_new = pd.DataFrame(daily_data, columns=columns)
    
    # 4. Combine and Deduplicate (The "Upsert" Magic)
    if not df_existing.empty:
        # Combine old data and new data
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        
        # Drop duplicates based on the Date and Issue Key. 
        # keep='last' ensures that if an issue changed status mid-day, the newer pull overwrites the morning pull.
        df_combined = df_combined.drop_duplicates(subset=['Date', 'Issue Key'], keep='last')
    else:
        df_combined = df_new
        
    # Fill any missing values with empty strings so Google Sheets doesn't throw an error
    df_combined = df_combined.fillna('')
        
    # 5. Overwrite the Google Sheet with the clean data
    worksheet.clear()
    
    # Convert dataframe back to a list of lists for gspread
    final_data = [df_combined.columns.values.tolist()] + df_combined.values.tolist()
    worksheet.update(values=final_data, range_name='A1')
    
    print(f"Successfully synced {len(df_combined)} total records without duplicates.")

if __name__ == "__main__":
    print("Authenticating with Jira...")
    jira_client = get_jira_client()
    
    print("Fetching latest issues...")
    daily_data = fetch_daily_sprint_data(jira_client)
    
    if daily_data:
        print("Upserting data to Google Sheets...")
        upsert_to_google_sheet(daily_data)
    else:
        print("No data found for today.")