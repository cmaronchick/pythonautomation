import streamlit as st
import nfl_data_py as nfl
import pandas as pd

st.set_page_config(layout="wide", page_title="NFL Timeout Analyzer")

st.title("🏈 NFL Timeout & Drive Success Dashboard")

# User inputs in the sidebar
years = st.sidebar.multiselect("Select Seasons", [2022, 2023, 2024, 2025], default=[2025])

@st.cache_data # This prevents reloading data every time you click a button
def load_data(years):
    pbp = nfl.import_pbp_data(years)
    # Basic cleanup: Filter for timeouts and merge drive results
    timeouts = pbp[pbp['timeout'] == 1].copy()
    drive_results = pbp.groupby(['game_id', 'drive'])['fixed_drive_result'].first().reset_index()
    df = pd.merge(timeouts, drive_results, on=['game_id', 'drive'], how='left')
    
    # Add Success Logic
    df['is_success'] = df['fixed_drive_result'].isin(['Touchdown', 'Field goal']).astype(int)
    return df

data = load_data(years)

# Team Filter
selected_team = st.selectbox("Select a Team to Inspect", options=sorted(data['timeout_team'].unique()))

# Filter the view
filtered_df = data[data['timeout_team'] == selected_team]

# Metrics
col1, col2 = st.columns(2)
col1.metric("Total Timeouts Called", len(filtered_df))
col2.metric("Drive Success Rate", f"{(filtered_df['is_success'].mean() * 100):.1f}%")

# Display the data table
st.subheader(f"Raw Timeout Data for {selected_team}")
st.dataframe(filtered_df[['week', 'qtr', 'half_seconds_remaining', 'yardline_100', 'fixed_drive_result']])

# Pivot Table for all teams
st.subheader("League-Wide Success Rates (Pivot)")
pivot = data.groupby('timeout_team')['is_success'].mean().sort_values(ascending=False)
st.bar_chart(pivot)