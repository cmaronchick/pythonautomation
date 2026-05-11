from jira import JIRA
import pandas as pd
from datetime import datetime
import config

# --- Configuration ---
JIRA_SERVER = 'https://2kcatd.atlassian.net/'
JIRA_EMAIL = 'christopher.aronchick@catdaddy.com'
JIRA_API_TOKEN = config.JIRA_API_TOKEN
FIX_VERSION = 'S8 Update 4'

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
    for issue in issues:
        # Extract fields
        issue_key = issue.key
        summary = issue.fields.summary
        status = issue.fields.status.name
        
        # Safely get story points (returns None if not estimated)
        story_points = getattr(issue.fields, STORY_POINTS_FIELD, 0)
        if story_points is None:
            story_points = 0
        # else:
        #     estimatedStories = estimatedStories + 1
            
        # Get the Epic Link (Custom field ID varies, often customfield_10014)
        # In newer Jira Cloud, Epic Link is often replaced by 'parent'
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

        data.append({
            'Date': today,
            'Issue Key': issue_key,
            'Epic': epic_key,
            'Parent Link': parent_link,
            'Summary': summary,
            'Status': status,
            'Story Points': story_points
        })

    return pd.DataFrame(data)

if __name__ == "__main__":
    print('starting)')
    jira_client = get_jira_client()
    df = fetch_daily_sprint_data(jira_client)
    # Assuming 'eoh_df' is your final DataFrame from the previous step
    filename = today + "-splash.csv"

    # Index=False prevents pandas from adding an extra column for the row numbers
    
    print(f"Extracted {len(df)} issues for fix version {FIX_VERSION}")
    print(df.head())
    df.to_csv(filename, index=False)
    
    
    # Save to CSV (append mode so you build a daily trend)
    # df.to_csv('burndown_data.csv', mode='a', header=not pd.io.common.file_exists('burndown_data.csv'), index=False)