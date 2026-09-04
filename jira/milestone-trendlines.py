import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.stats import linregress
from datetime import datetime

# 1. Load Data
df = pd.read_csv("Splash_Daily_Jira_Burndown_with_Milestones.csv")
df['Date'] = pd.to_datetime(df['Date'])
burndown_data = df.groupby(['Date', 'Milestone'])['Remaining Story Points'].sum().reset_index()

# 2. Setup Plot & Targets
plt.figure(figsize=(10, 6))
milestones = {
    'First Playable (Sep 11)': ('2026-09-11', '#1f77b4'), # Blue
    'Feature Complete (Oct 2)': ('2026-10-02', '#ff7f0e'), # Orange
    'Content Complete (Oct 9)': ('2026-10-09', '#2ca02c')  # Green
}

# 3. Plot Actuals and Projections
for milestone, (target_str, color) in milestones.items():
    m_data = burndown_data[burndown_data['Milestone'] == milestone].sort_values('Date')
    if m_data.empty: continue
        
    x_hist = m_data['Date']
    y_hist = m_data['Remaining Story Points']
    target_date = pd.to_datetime(target_str)
    
    # Plot Actuals
    plt.plot(x_hist, y_hist, label=f"{milestone} (Actual)", color=color, linewidth=2)
    
    # Calculate & Plot Projections
    slope, intercept, _, _, _ = linregress(x_hist.map(datetime.toordinal), y_hist)
    last_date = x_hist.max()
    
    if last_date < target_date:
        future_dates = pd.date_range(start=last_date, end=target_date)
        future_y = np.maximum(slope * future_dates.map(datetime.toordinal) + intercept, 0)
        plt.plot(future_dates, future_y, linestyle='--', color=color)
        plt.axvline(x=target_date, color=color, linestyle=':', alpha=0.6)

# 4. Format and Save
plt.title('Milestone Burndown Projections', fontsize=14, pad=15)
plt.xlabel('Date')
plt.ylabel('Remaining Story Points')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
plt.tight_layout()
plt.savefig('presentation_chart.png', dpi=300) # High-res for presentations
