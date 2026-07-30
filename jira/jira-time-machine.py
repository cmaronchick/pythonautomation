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

# --- 1. TEMPORARY CREDENTIALS (DO NOT COMMIT THIS FILE TO GIT) ---
# Paste your actual credentials here just for this one-time run
JIRA_SERVER = 'https://2kcatd.atlassian.net/'
JIRA_EMAIL = 'christopher.aronchick@catdaddy.com'
JIRA_API_TOKEN = 'Dummy'


# Paste the ENTIRE JSON string from your Google Service Account here
GOOGLE_CREDS_JSON_STRING = "Dummy"

DRIVE_FILE_ID = '1LpmkksTQ6MbrPeu5vmDRMW7OA7rA04XI' 
# https://docs.google.com/spreadsheets/d/1LpmkksTQ6MbrPeu5vmDRMW7OA7rA04XI/edit?usp=sharing&ouid=113460444391050411114&rtpof=true&sd=true
# https://docs.google.com/spreadsheets/d/11gxwbPL4_UV0AUxSXpBF3VQtBesvOS2_/edit?usp=drive_link&ouid=113460444391050411114&rtpof=true&sd=true
SHEET_NAME = 'Data' 

# --- 2. CONFIGURATION ---
START_DATE_LIMIT = '2026-06-15' # Only save data from this date forward
STORY_POINTS_FIELD = 'customfield_10026' 
SEVERITY_FIELD = 'customfield_10030'
DONE_STATUSES = ['Done', 'Closed', 'Claim Fix', 'Will Not Fix', 'Duplicate', 'Deferred', 'Not A Bug']


# Paste your exact JQL here (without the fixVersion filtering you removed)
JQL_QUERY = 'project = SPLASH AND issueType in (Story, Task, Bug)' 

def get_jira_client():
    return JIRA(server=JIRA_SERVER, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))

def build_historical_timeline(jira):
    
    fieldsPrinted = False
    print(f"Fetching issues and changelogs... (This might take a minute)")
    issues = jira.search_issues(JQL_QUERY, expand='changelog', maxResults=False)
    
    historical_records = []
    today = datetime.now()
    
    secondParentPrinted = 0
    for issue in issues:
        # 1. Grab the static fields that don't change daily
        story_points = getattr(issue.fields, STORY_POINTS_FIELD, 0)
        epic_key = issue.fields.parent.key if hasattr(issue.fields, 'parent') else "No Epic"
        parent_link = getattr(issue.fields, 'customfield_10014', epic_key) 
        status_name = issue.fields.status.name
        issue_type = issue.fields.issuetype.name
        created_raw = issue.fields.created
        created_date_str = created_raw[:10] if created_raw else today.strftime('%Y-%m-%d')
        created_date = datetime.strptime(created_date_str, '%Y-%m-%d')
        
        fix_versions_list = issue.fields.fixVersions
        fix_versions_str = ", ".join([fv.name for fv in fix_versions_list]) if fix_versions_list else ""
        priority = issue.fields.priority.name if hasattr(issue.fields, 'priority') and issue.fields.priority else "None"
        severity_raw = getattr(issue.fields, SEVERITY_FIELD, None)
        severity = severity_raw.value if hasattr(severity_raw, 'value') else (severity_raw if isinstance(severity_raw, str) else "None")
        summary = issue.fields.summary

        # 2. Determine Current State
        current_status = issue.fields.status.name
        current_points = getattr(issue.fields, STORY_POINTS_FIELD, 0)
        current_points = float(current_points) if current_points is not None else 0.0

        # 3. Sort the changelog from oldest to newest
        histories = sorted(issue.changelog.histories, key=lambda h: h.created)
        
        status_changes_by_date = {}
        points_changes_by_date = {}
        
        initial_status = current_status
        initial_points = current_points
        
        if epic_key != "No Epic":
            # fields = issueObj.fields
            parent = getattr(issue.fields, 'parent')
            # print('parent fields: ', parent.raw)
            parent_link = getattr(parent.fields, 'summary')
            parentFields = issue.fields.parent.raw
            issueFields = issue.fields
            if fieldsPrinted == False:
                print('issue with epic: ', parentFields)
                print('issueFields: ',issueFields)
                print(dir(issue), {
                    'Date': today,
                    'Issue Key': issue.key,
                    'Epic': epic_key,
                    'Parent Link': parent_link,
                    'Summary': issue.fields.summary,
                    'Status': status_name,
                    'Story Points': story_points if story_points is not None else 0,
                    'Issue Type': issue_type,
                    'Created Date': created_date,
                    'Fix Versions': fix_versions_str, # NEW: Add to the dictionary
                    'Priority': priority,          # Added to dictionary
                    'Severity': severity          # Added to dictionary
                })
                fieldsPrinted = True

        # 4. Extract the changes
        for history in histories:
            change_date = history.created[:10]
            for item in history.items:
                if item.field == 'status':
                    # If this is the very first status change, the 'fromString' is our initial creation status
                    if initial_status == current_status and item.fromString: 
                        initial_status = item.fromString
                    status_changes_by_date[change_date] = item.toString
                elif item.field == 'Story Points' or item.field == STORY_POINTS_FIELD:
                    if initial_points == current_points and item.fromString:
                        try: initial_points = float(item.fromString)
                        except: pass
                    try: points_changes_by_date[change_date] = float(item.toString) if item.toString else 0.0
                    except: pass

        # 5. Forward-Fill the Timeline
        date_range = pd.date_range(start=created_date, end=today)
        cutoff_date = datetime.strptime(START_DATE_LIMIT, '%Y-%m-%d') # NEW
        
        running_status = initial_status
        running_points = initial_points
        for dt in date_range:
            d_str = dt.strftime('%m/%d/%Y')
            
            # Did it change on this specific day?
            if d_str in status_changes_by_date:
                running_status = status_changes_by_date[d_str]
            if d_str in points_changes_by_date:
                running_points = points_changes_by_date[d_str]
            # 2. NEW: If this date is before our cutoff limit, just skip to the next day!
            if dt < cutoff_date:
                continue
                
            remaining_points = 0.0 if running_status in DONE_STATUSES else running_points
            if parent_link != "No Epic" and secondParentPrinted < 10:
                print('parent_link:', parent_link)
                print('secondParentPrinted: ', secondParentPrinted)
                
            secondParentPrinted = secondParentPrinted + 1
            historical_records.append({
                'Date': dt.date(),
                'Issue Key': issue.key,
                'Epic': epic_key,
                'Parent Link': parent_link,
                'Summary': issue.fields.summary,
                'Status': running_status,
                'Story Points': running_points,
                'Issue Type': issue_type,
                'Created Date': created_date,
                'Fix Versions': fix_versions_str, # NEW: Add to the dictionary
                'Priority': priority,          # Added to dictionary
                'Severity': severity,          # Added to dictionary'Status': running_status,
                'Remaining Story Points': remaining_points
            })
            

    return pd.DataFrame(historical_records)

# def overwrite_google_drive(df_new_history):
#     creds_dict = json.loads(GOOGLE_CREDS_JSON_STRING, strict=False)
#     credentials = service_account.Credentials.from_service_account_info(
#         creds_dict, scopes=['https://www.googleapis.com/auth/drive']
#     )
#     drive_service = build('drive', 'v3', credentials=credentials)

#     print("Downloading existing Excel file...")
#     request = drive_service.files().get_media(fileId=DRIVE_FILE_ID)
#     fh = io.BytesIO()
#     downloader = MediaIoBaseDownload(fh, request)
#     done = False
#     while not done:
#         _, done = downloader.next_chunk()
    
#     fh.seek(0)
#     temp_filename = 'temp_history_rebuild.xlsx'
#     with open(temp_filename, 'wb') as f:
#         f.write(fh.read())

#     # We enforce the exact columns so your PivotTables don't break
#     expected_cols = ['Date', 'Issue Key', 'Epic', 'Parent Link', 'Summary', 'Status', 'Story Points', 'Issue Type', 'Created Date', 'Fix Versions', 'Priority', 'Severity', 'Remaining Story Points']
#     for col in expected_cols:
#         if col not in df_new_history.columns:
#             df_new_history[col] = ""
#     df_new_history = df_new_history[expected_cols]

#     print(f"Rebuilding Excel Data tab with {len(df_new_history)} historical records...")
#     # We use if_sheet_exists='replace' to completely overwrite the old Data tab with this new perfect history
#     with pd.ExcelWriter(temp_filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
#         df_new_history.to_excel(writer, sheet_name=SHEET_NAME, index=False)

#     print("Uploading back to Google Drive...")
#     media = MediaFileUpload(
#         temp_filename, 
#         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
#         resumable=True
#     )
    
#     drive_service.files().update(fileId=DRIVE_FILE_ID, media_body=media).execute()
    
#     # if os.path.exists(temp_filename):
#     #     os.remove(temp_filename)
        
#     print("Success! Time Machine complete.")

def overwrite_google_drive(df_new_history):
    # Enforce the exact columns so your PivotTables don't break
    expected_cols = ['Date', 'Issue Key', 'Epic', 'Parent Link', 'Summary', 'Status', 'Story Points', 'Issue Type', 'Created Date', 'Fix Versions', 'Priority', 'Severity', 'Remaining Story Points']
    for col in expected_cols:
        if col not in df_new_history.columns:
            df_new_history[col] = ""
    df_new_history = df_new_history[expected_cols]

    local_filename = 'time_machine_export.xlsx'
    
    print(f"Saving {len(df_new_history)} historical records to a local file...")
    
    # Writing to a brand new file is extremely fast and uses almost no memory
    df_new_history.to_excel(local_filename, index=False)
    
    print(f"Success! Your history is saved as '{local_filename}' in the same folder as this script.")
    print("Next Step: Open that file, copy all the rows, and paste them over the 'Data' tab in your Google Drive file!")

if __name__ == "__main__":
    jira_client = get_jira_client()
    df_history = build_historical_timeline(jira_client)
    overwrite_google_drive(df_history)