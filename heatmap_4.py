import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load the dataset
file_path = r'E:\CompAppTools\Project\TehranWeather.xlsx'
df = pd.read_excel(file_path)

# Convert the 'date' column to datetime
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

# Prepare the data for each season and ensure consistency in length
resampled_seasons = {}
for season, data in seasons.items():
    resampled_seasons[season] = data.set_index('date').resample('D').mean()['tavg']

# Convert the resampled data to a DataFrame where each season is a column
season_matrix = pd.DataFrame({
    'Winter': resampled_seasons['Winter'],
    'Spring': resampled_seasons['Spring'],
    'Summer': resampled_seasons['Summer'],
    'Fall': resampled_seasons['Fall']
})

# Ensure all seasons have the same length using forward-fill and backward-fill
season_matrix = season_matrix.fillna(method='ffill').fillna(method='bfill')

# Plot the heatmap using Matplotlib
fig, ax = plt.subplots(figsize=(10, 6))

# Create a colormap from blue (cold) to red (warm)
cmap = plt.get_cmap("coolwarm")

# Plot the heatmap without interpolation
cax = ax.imshow(season_matrix.T, cmap=cmap, aspect='auto', interpolation='none')

# Add color bar for temperature scale
cbar = plt.colorbar(cax, ax=ax, label='Temperature (°C)', pad=0.02)
cbar.ax.tick_params(labelsize=10)

# Add labels and title
ax.set_title('Seasonal Temperature Heatmap', fontsize=16, fontweight='bold')
ax.set_xlabel('Day of Year', fontsize=14)
ax.set_ylabel('Season', fontsize=14)

# Set the x-ticks and y-ticks labels
x_ticks = np.linspace(0, len(season_matrix) - 1, 5).astype(int)
x_labels = pd.date_range(start='2024-01-01', periods=len(season_matrix), freq='D').strftime('%d-%b')[x_ticks]
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, rotation=45, fontsize=10)

ax.set_yticks(np.arange(4))
ax.set_yticklabels(['Winter', 'Spring', 'Summer', 'Fall'], fontsize=12)

# Add a caption below the plot
caption = "This heatmap represents the average daily temperatures across seasons in Tehran for the year 2024."
plt.figtext(0.5, -0.02, caption, wrap=True, horizontalalignment='center', fontsize=14, color='black')

# Ensure layout is tight
plt.tight_layout(rect=[0, 0.05, 1, 1])  # Adjust layout to fit caption

# Save the figure as a PDF
output_path = r'E:\CompAppTools\FinalProject-MH\Final_Project_CMSC6950\Seasonal_Temperature_Heatmap.pdf'
plt.savefig(output_path, format='pdf', bbox_inches='tight')

# Show the plot
plt.show()