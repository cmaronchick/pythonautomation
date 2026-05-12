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
            print('parent fields: ', parent.raw)
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

def append_to_google_sheet(data):
    # Load credentials from the GitHub Secret JSON string
    creds_json = os.environ['GOOGLE_CREDENTIALS']
    creds_dict = json.loads(creds_json)
    
    # Authenticate with Google
    gc = gspread.service_account_from_dict(creds_dict)
    
    # Open the sheet and target tab
    sh = gc.open_by_key(GOOGLE_SHEET_ID)
    worksheet = sh.worksheet(SHEET_TAB_NAME)
    
    # Append the new rows at the bottom of the sheet
    worksheet.append_rows(data)
    print(f"Successfully added {len(data)} rows to Google Sheets.")

if __name__ == "__main__":
    print("Authenticating with Jira...")
    jira_client = get_jira_client()
    
    print("Fetching issues...")
    daily_data = fetch_daily_sprint_data(jira_client)
    
    if daily_data:
        print("Uploading to Google Sheets...")
        append_to_google_sheet(daily_data)
    else:
        print("No data found for today.")