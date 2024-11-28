import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate  # For pretty-printing tables

# Load the dataset
file_path = r'E:\CompAppTools\Project\TehranWeather.xlsx'
df = pd.read_excel(file_path)

# Check the first few rows of the data to confirm it has loaded correctly
print(df.head())

# Assuming 'date' column is in the format 'YYYY-MM-DD', convert it to datetime
df['date'] = pd.to_datetime(df['date'])

# Define seasonal date ranges
winter = (df['date'] >= '2023-12-21') & (df['date'] <= '2024-03-20')
spring = (df['date'] >= '2024-03-21') & (df['date'] <= '2024-06-20')
summer = (df['date'] >= '2024-06-21') & (df['date'] <= '2024-09-20')
fall = (df['date'] >= '2024-09-21') & (df['date'] <= '2024-12-20')

# Segment the dataset by seasons
seasons = {
    'Winter': df[winter],
    'Spring': df[spring],
    'Summer': df[summer],
    'Fall': df[fall]
}

# Initialize an empty list to store statistics
season_stats = []

# Calculate the statistics for each season
for season, data in seasons.items():
    temp_stats = {
        'Season': season,
        'Min Temp (°C)': data['tavg'].min(),
        'Max Temp (°C)': data['tavg'].max(),
        'Mean Temp (°C)': data['tavg'].mean(),
        'Median Temp (°C)': data['tavg'].median(),
        'Std Temp (°C)': data['tavg'].std(),
        'Min Precip (mm)': data['prcp'].min(),
        'Max Precip (mm)': data['prcp'].max(),
        'Mean Precip (mm)': data['prcp'].mean(),
        'Median Precip (mm)': data['prcp'].median(),
        'Std Precip (mm)': data['prcp'].std(),
        'Min Wind Speed (m/s)': data['wspd'].min(),
        'Max Wind Speed (m/s)': data['wspd'].max(),
        'Mean Wind Speed (m/s)': data['wspd'].mean(),
        'Median Wind Speed (m/s)': data['wspd'].median(),
        'Std Wind Speed (m/s)': data['wspd'].std(),
    }
    season_stats.append(temp_stats)

# Convert to DataFrame for better display
season_stats_df = pd.DataFrame(season_stats)

# Adding a caption for the table
print("\nTable 2: Seasonal Statistics of Temperature, Precipitation, and Wind Speed")
print(tabulate(season_stats_df, headers='keys', tablefmt='grid'))

# Plotting grouped bar chart for temperature, precipitation, and wind speed
x = np.arange(len(season_stats_df['Season']))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots(figsize=(14, 8))

# Plotting offset bars for temperature, precipitation, and wind speed
temp_bars = ax.bar(x - width, season_stats_df['Mean Temp (°C)'], width, label='Mean Temp', color='tab:blue', alpha=0.8)
precip_bars = ax.bar(x, season_stats_df['Mean Precip (mm)'], width, label='Mean Precip', color='tab:green', alpha=0.8)
wspd_bars = ax.bar(x + width, season_stats_df['Mean Wind Speed (m/s)'], width, label='Mean Wind Speed', color='tab:orange', alpha=0.8)

# Add labels, title, and legend
ax.set_xlabel('Season')
ax.set_ylabel('Values')
ax.set_title('Seasonal Temperature, Precipitation, and Wind Speed Statistics')
ax.set_xticks(x)
ax.set_xticklabels(season_stats_df['Season'])
ax.legend()

# Annotate bar values for each variable
for bar in temp_bars:
    ax.annotate(f'{bar.get_height():.1f}', xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 3), textcoords="offset points", ha='center', fontsize=9)
for bar in precip_bars:
    ax.annotate(f'{bar.get_height():.1f}', xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 3), textcoords="offset points", ha='center', fontsize=9)
for bar in wspd_bars:
    ax.annotate(f'{bar.get_height():.1f}', xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 3), textcoords="offset points", ha='center', fontsize=9)

# Adding a table to the figure
table_data = season_stats_df.set_index('Season').round(2)  # Format values to 2 decimal points
table = plt.table(cellText=table_data.values,
                  colLabels=table_data.columns,
                  rowLabels=table_data.index,
                  cellLoc='center',
                  loc='bottom',
                  bbox=[0, -0.5, 1, 0.3])  # Adjust bbox for positioning

table.auto_set_font_size(False)
table.set_fontsize(8)

# Adding a comprehensive caption below the figure and table
caption_text = (
    "Figure and Table: Seasonal Temperature, Precipitation, and Wind Speed Statistics\n"
    "The figure shows the average temperature (°C), precipitation (mm), and wind speed (m/s) across seasons (Winter, Spring, Summer, and Fall) as grouped bar charts. "
    "The table below summarizes detailed seasonal statistics, including minimum, maximum, mean, median, and standard deviation for each variable. "
    "The data is derived from Tehran's weather dataset, highlighting seasonal variations in climate parameters."
)

fig.text(0.5, -0.01, caption_text, ha='center', fontsize=14, wrap=True)  # Adjust the vertical position as needed

# Save the figure as a PDF
output_path = r'E:\CompAppTools\Project\Seasonal_Statistics.pdf'
plt.savefig(output_path, format='pdf', bbox_inches='tight')

fig.tight_layout()
plt.show()