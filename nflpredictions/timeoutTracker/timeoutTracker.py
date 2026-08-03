import nfl_data_py as nfl
import pandas as pd

def get_timeout_success_metrics(years=[2025]):
    pbp = nfl.import_pbp_data(years)
    
    # Check if 'fixed_drive_result' exists; if not, use 'drive_result'
    # 'drive_result' is the standard raw column
    result_col = 'fixed_drive_result' if 'fixed_drive_result' in pbp.columns else 'drive_result'
    
    # 1. Filter for timeouts
    timeouts = pbp[pbp['timeout'] == 1].copy()
    
    # 2. Get Drive Results
    # We use .fillna('Unknown') to prevent merge issues if data is missing
    drive_results = pbp.groupby(['game_id', 'drive'])[result_col].first().reset_index()
    drive_results.columns = ['game_id', 'drive', 'final_result']
    
    # 3. Merge
    df = pd.merge(timeouts, drive_results, on=['game_id', 'drive'], how='left')
    
    # 4. Success Logic (Case-insensitive to handle different naming conventions)
    success_keywords = ['TOUCHDOWN', 'FIELD GOAL', 'TD', 'FG']
    df['is_success'] = df['final_result'].str.upper().str.contains('|'.join(success_keywords), na=False).astype(int)
    
    return df

# Pull data for the current season
timeout_df = get_timeout_success_metrics([2025])

# 6. Calculate Success Rate by Team
team_metrics = timeout_df.groupby('timeout_team').agg({
    'is_success': ['count', 'sum', 'mean']
})

# Flatten columns for readability
team_metrics.columns = ['Total Timeouts', 'Scoring Drives', 'Success Rate (%)']
team_metrics['Success Rate (%)'] = (team_metrics['Success Rate (%)'] * 100).round(2)

# Sort by highest success rate
print(team_metrics.sort_values(by='Success Rate (%)', ascending=False).head(10))

# Assuming 'eoh_df' is your final DataFrame from the previous step
filename = "nfl_timeout_analysis_2025.csv"

# Index=False prevents pandas from adding an extra column for the row numbers
timeout_df.to_csv(filename, index=False)

print(f"Success! Data exported to {filename}")