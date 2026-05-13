import os
import json
import io
import pandas as pd
from datetime import datetime
from jira import JIRA
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
# import config

# --- Configuration ---
JIRA_SERVER = 'https://2kcatd.atlassian.net/'
JIRA_EMAIL = 'christopher.aronchick@catdaddy.com'
JIRA_API_TOKEN = os.environ['JIRA_API_TOKEN']
FIX_VERSION = 'S8 Update 4'
STORY_POINTS_FIELD = 'customfield_10026' 
DRIVE_FILE_ID = '1WulP_8RKqm5r7TlIsnGjZ2KIg2NfBA2c' # Paste your ID here
SHEET_NAME = 'Data' # Change if your tab is named differently

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
    
    # JQL to find all issues in the fix version. 
    # You can add 'AND Sprint in openSprints()' if you only want active sprint tasks
    jql_query = f'fixVersion = "{FIX_VERSION}" AND issueType in (Story, Task, Bug)'
    
    # maxResults=False handles pagination automatically in the python-jira library
    issues = jira.search_issues(jql_query, maxResults=False)
    
    ### use this to check for custom fields

    fields = jira.fields()
    for field in fields:
        print(f"ID: {field['id']}, Name: {field['name']}")
    print('issues: ', len(issues))
    data = []
    
    fieldsPrinted = False 
    # for issue in issues:
    #     # Extract fields
    #     issue_key = issue.key
    #     summary = issue.fields.summary
    #     status = issue.fields.status.name
        
    #     # Safely get story points (returns None if not estimated)
    #     story_points = getattr(issue.fields, STORY_POINTS_FIELD, 0)
    #     if story_points is None:
    #         story_points = 0
    #     # else:
    #     #     estimatedStories = estimatedStories + 1
            
    #     # Get the Epic Link (Custom field ID varies, often customfield_10014)
    #     # In newer Jira Cloud, Epic Link is often replaced by 'parent'
    #     epic_key = issue.fields.parent.key if hasattr(issue.fields, 'parent') else "No Epic"
    #     parent_link = ''
    #     if epic_key != "No Epic":
    #         # fields = issueObj.fields
    #         parent = getattr(issue.fields, 'parent')
    #         print('parent fields: ', parent.raw)
    #         parent_link = getattr(parent.fields, 'summary')
    #         if fieldsPrinted == False:
    #             print(dir(issue))
    #             print('issue with epic: ', issue.fields.parent.raw)
    #         #     for field in fields:
    #         #         print(f"ID: {field['id']}, Name: {field['name']}")
    #             fieldsPrinted = True

    #     data.append([
    #         today,
    #         issue.key,
    #         epic_key,
    #         parent_link,
    #         issue.fields.summary,
    #         issue.fields.status.name,
    #         story_points if story_points is not None else 0
    #     ])

    for issue in issues:
        story_points = getattr(issue.fields, STORY_POINTS_FIELD, 0)
        epic_key = issue.fields.parent.key if hasattr(issue.fields, 'parent') else "No Epic"
        parent_link = ''
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

        data.append([
            today,
            issue.key,
            epic_key,
            parent_link,
            issue.fields.summary,
            issue.fields.status.name,
            story_points if story_points is not None else 0
        ])
    return data

    return data

def upsert_to_google_drive_excel(daily_data):
    # 1. Authenticate with Google Drive
    creds_json = os.environ['GOOGLE_CREDENTIALS']
    creds_dict = json.loads(creds_json)
    credentials = service_account.Credentials.from_service_account_info(
        creds_dict, scopes=['https://www.googleapis.com/auth/drive']
    )
    drive_service = build('drive', 'v3', credentials=credentials)

    # 2. Download the existing Excel file into memory
    print("Downloading Excel file from Google Drive...")
    request = drive_service.files().get_media(fileId=DRIVE_FILE_ID)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    
    fh.seek(0)
    
    # 3. Save it temporarily so we can safely edit it
    temp_filename = 'temp_burndown.xlsx'
    with open(temp_filename, 'wb') as f:
        f.write(fh.read())

    # 4. Upsert Data (Remove duplicates, keep latest)
    df_new = pd.DataFrame(daily_data)
    
    try:
        df_existing = pd.read_excel(temp_filename, sheet_name=SHEET_NAME)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        # Drop duplicates based on Date and Issue Key
        df_combined = df_combined.drop_duplicates(subset=['Date', 'Issue Key'], keep='last')
    except Exception as e:
        print(f"Could not read existing data (might be empty): {e}")
        df_combined = df_new

    # 5. Safely write back to the Excel file, replacing ONLY the Data sheet 
    # (This preserves your PivotCharts on the other tabs!)
    print("Updating Excel data...")
    with pd.ExcelWriter(temp_filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df_combined.to_excel(writer, sheet_name=SHEET_NAME, index=False)

    # 6. Upload the modified file back to Google Drive
    print("Uploading updated file to Google Drive...")
    media = MediaFileUpload(temp_filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    drive_service.files().update(
        fileId=DRIVE_FILE_ID,
        media_body=media
    ).execute()
    
    # Cleanup temp file
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