import os
import json
import io
import time
import pandas as pd
from datetime import datetime
from jira import JIRA
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload


# --- Configuration ---
JIRA_SERVER = 'https://2kcatd.atlassian.net/'
JIRA_EMAIL = 'christopher.aronchick@catdaddy.com'
JIRA_API_TOKEN = os.environ['JIRA_API_TOKEN']
FIX_VERSION = 'S8 Update 4'
STORY_POINTS_FIELD = 'customfield_10026' 
DRIVE_FILE_ID = '1WulP_8RKqm5r7TlIsnGjZ2KIg2NfBA2c' # Paste your ID here
SHEET_NAME = 'Data' # Change if your tab is named differently

# Define what "Done" means in your Jira instance
DONE_STATUSES = ['Done', 'Closed', 'Resolved']

# The custom field ID for Story Points varies by Jira instance.
# You can find yours by looking at the JSON of a single issue via the API.
STORY_POINTS_FIELD = 'customfield_10026' 
today = datetime.now().strftime('%Y-%m-%d')
estimatedStories = 0

def get_jira_client():
    return JIRA(
        server=JIRA_SERVER,
        basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
    )

def fetch_daily_sprint_data(jira):
    jql_query = f'fixVersion = "{FIX_VERSION}" AND issueType in (Story, Task, Bug)'
    issues = jira.search_issues(jql_query, maxResults=False)
    
    data = []
    today = datetime.now().strftime('%Y-%m-%d')

    for issue in issues:
        story_points = getattr(issue.fields, STORY_POINTS_FIELD, 0)
        epic_key = issue.fields.parent.key if hasattr(issue.fields, 'parent') else "No Epic"
        status_name = issue.fields.status.name
        parent_link = getattr(issue.fields, 'customfield_10014', epic_key)
        if epic_key != "No Epic":
            # fields = issueObj.fields
            parent = getattr(issue.fields, 'parent')
            # print('parent fields: ', parent.raw)
            parent_link = getattr(parent.fields, 'summary')
            if fieldsPrinted == False:
                print(dir(issue))
                print('issue with epic: ', issue.fields.parent.raw)
            #     for field in fields:
            #         print(f"ID: {field['id']}, Name: {field['name']}")
                fieldsPrinted = True


        data.append({
            'Date': today,
            'Issue Key': issue.key,
            'Epic': epic_key,
            'Parent Link': parent_link,
            'Summary': issue.fields.summary,
            'Status': status_name,
            'Story Points': story_points if story_points is not None else 0
        })
    return data

def upsert_to_google_drive_excel(daily_data):
    creds_json = os.environ['GOOGLE_CREDENTIALS']
    creds_dict = json.loads(creds_json)
    credentials = service_account.Credentials.from_service_account_info(
        creds_dict, scopes=['https://www.googleapis.com/auth/drive']
    )
    drive_service = build('drive', 'v3', credentials=credentials)

    print("Downloading Excel file from Google Drive...")
    request = drive_service.files().get_media(fileId=DRIVE_FILE_ID)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    
    fh.seek(0)
    temp_filename = 'temp_burndown.xlsx'
    with open(temp_filename, 'wb') as f:
        f.write(fh.read())

    # Added the new column to our expected columns
    expected_cols = ['Date', 'Issue Key', 'Epic', 'Parent Link', 'Summary', 'Status', 'Story Points', 'Remaining Story Points']
    df_new = pd.DataFrame(daily_data)
    
    for col in expected_cols:
        if col not in df_new.columns:
            df_new[col] = ""
            
    df_new = df_new[expected_cols]

    try:
        df_existing = pd.read_excel(temp_filename, sheet_name=SHEET_NAME)
        df_existing = df_existing.loc[:, ~df_existing.columns.astype(str).str.contains('^Unnamed')]
        df_existing = df_existing.loc[:, ~df_existing.columns.astype(str).str.match(r'^\d+$')]
        
        for col in expected_cols:
            if col not in df_existing.columns:
                df_existing[col] = ""
        df_existing = df_existing[expected_cols]

        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined['Date'] = pd.to_datetime(df_combined['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
        df_combined = df_combined.dropna(subset=['Date', 'Issue Key'])
        df_combined = df_combined.drop_duplicates(subset=['Date', 'Issue Key'], keep='last')
        
    except Exception as e:
        print(f"Could not read existing data cleanly: {e}")
        df_combined = df_new

    # THE FIX: Calculate "Remaining Story Points" dynamically for the entire historical dataset
    df_combined['Story Points'] = pd.to_numeric(df_combined['Story Points'], errors='coerce').fillna(0)
    df_combined['Remaining Story Points'] = df_combined.apply(
        lambda row: 0 if str(row['Status']) in DONE_STATUSES else row['Story Points'], 
        axis=1
    )

    df_combined = df_combined[expected_cols]

    print("Updating Excel data...")
    latest_date = df_combined['Date'].max()
    df_current_state = df_combined[df_combined['Date'] == latest_date]

    with pd.ExcelWriter(temp_filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df_combined.to_excel(writer, sheet_name=SHEET_NAME, index=False)
        df_current_state.to_excel(writer, sheet_name='Current State', index=False)

    print("Uploading updated file to Google Drive...")
    media = MediaFileUpload(
        temp_filename, 
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        resumable=True
    )
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            drive_service.files().update(
                fileId=DRIVE_FILE_ID,
                media_body=media
            ).execute()
            print("Upload successful!")
            break
        except Exception as e:
            print(f"Upload attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                raise

    if os.path.exists(temp_filename):
        os.remove(temp_filename)
        
    print(f"Success! Deduplicated and synced {len(df_combined)} total records.")

if __name__ == "__main__":
    print("Authenticating with Jira...")
    jira_client = get_jira_client()
    
    print("Fetching latest issues...")
    daily_data = fetch_daily_sprint_data(jira_client)
    
    if daily_data:
        print("Upserting data to Google Sheets...")
        upsert_to_google_drive_excel(daily_data)
    else:
        print("No data found for today.")