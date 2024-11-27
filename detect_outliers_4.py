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
    'Winter': df[winter]['tavg'],
    'Spring': df[spring]['tavg'],
    'Summer': df[summer]['tavg'],
    'Fall': df[fall]['tavg']
}

# Prepare the data for each season
seasons_data = [seasons['Winter'], seasons['Spring'], seasons['Summer'], seasons['Fall']]

# Define colors for each season
box_colors = ['skyblue', 'lightgreen', 'lightcoral', 'lightsalmon']

# Function to calculate Z-Score and IQR outliers
def detect_outliers(data):
    # Z-Score method (±1.5 standard deviations)
    mean = np.mean(data)
    std = np.std(data)
    z_upper = mean + 1.5 * std
    z_lower = mean - 1.5 * std
    z_outliers = data[(data > z_upper) | (data < z_lower)]
    
    # IQR method
    q1, q3 = np.percentile(data, [25, 75])
    iqr = q3 - q1
    iqr_upper = q3 + 1.5 * iqr
    iqr_lower = q1 - 1.5 * iqr
    iqr_outliers = data[(data > iqr_upper) | (data < iqr_lower)]
    
    return z_outliers, iqr_outliers, mean, std

# Create a figure with two subplots (before and after removing outliers)
fig, axs = plt.subplots(1, 2, figsize=(16, 9))

# Plot Before Removing Outliers
axs[0].set_title('Temperature Distribution by Season (Before Removing Outliers)', fontsize=16, fontweight='bold', color='darkblue')
axs[0].set_ylabel('Temperature (°C)', fontsize=14, fontweight='bold', color='darkblue')
axs[0].set_xlabel('Season', fontsize=14, fontweight='bold', color='darkblue')

# Create the boxplot (Before Removing Outliers)
bp = axs[0].boxplot(seasons_data, labels=['Winter', 'Spring', 'Summer', 'Fall'], patch_artist=True,
                    boxprops=dict(facecolor='lightgray', color='black'), whiskerprops=dict(color='black', linewidth=1.5),
                    flierprops=dict(markerfacecolor='red', marker='o', markersize=8, linestyle='none'),
                    medianprops=dict(color='black', linewidth=2))

# Assign colors to each boxplot
for patch, color in zip(bp['boxes'], box_colors):
    patch.set_facecolor(color)

# Add scatter plots and annotate outliers (Before Removing)
for i, season_data in enumerate(seasons_data):
    jitter = np.random.normal(0, 0.03, len(season_data))  # Add slight horizontal jitter
    
    # Scatter individual data points
    axs[0].scatter([i + 1 + jitter_offset for jitter_offset in jitter], season_data,
                   color='black', alpha=0.6, s=15)

    # Detect outliers using both methods
    z_outliers, iqr_outliers, mean, std = detect_outliers(season_data)
    
    # Plot Z-Score outliers
    axs[0].scatter([i + 1] * len(z_outliers), z_outliers, color='gold', edgecolor='black', s=50, label='Z-Score Outlier')

    # Plot IQR outliers (now explicitly set to orange)
    axs[0].scatter([i + 1] * len(iqr_outliers), iqr_outliers, color='orange', edgecolor='black', s=50, label='IQR Outlier')

    # Annotate mean and std
    axs[0].text(i + 1, mean + 0.3, f'Mean: {mean:.2f}', ha='center', va='bottom', color='darkblue', fontsize=12, fontweight='bold')
    axs[0].text(i + 1, mean - 0.3, f'Std: {std:.2f}', ha='center', va='top', color='darkred', fontsize=12, fontweight='bold')

# Plot After Removing Outliers
axs[1].set_title('Temperature Distribution by Season (After Removing Outliers)', fontsize=16, fontweight='bold', color='darkblue')
axs[1].set_ylabel('Temperature (°C)', fontsize=14, fontweight='bold', color='darkblue')
axs[1].set_xlabel('Season', fontsize=14, fontweight='bold', color='darkblue')

# Remove outliers and plot
seasons_no_outliers = []
total_removed = 0  # Variable to keep track of total removed outliers
season_names = ['Winter', 'Spring', 'Summer', 'Fall']

for season_data, season_name in zip(seasons_data, season_names):
    z_outliers, iqr_outliers, mean, std = detect_outliers(season_data)
    clean_data = season_data[~season_data.isin(z_outliers) & ~season_data.isin(iqr_outliers)]
    seasons_no_outliers.append(clean_data)
    
    # Calculate percentage of removed data
    removed_data = len(season_data) - len(clean_data)
    total_removed += removed_data
    print(f"Removed {removed_data} outliers from {season_name} data (Total {removed_data / len(season_data) * 100:.2f}% removed)")

# Calculate the total percentage of removed data across all seasons
total_data_points = sum(len(season_data) for season_data in seasons_data)
percentage_removed = (total_removed / total_data_points) * 100
print(f"\nTotal percentage of data removed as outliers: {percentage_removed:.2f}%")

# Create the boxplot (After Removing Outliers)
bp = axs[1].boxplot(seasons_no_outliers, labels=['Winter', 'Spring', 'Summer', 'Fall'], patch_artist=True,
                    boxprops=dict(facecolor='lightgray', color='black'), whiskerprops=dict(color='black', linewidth=1.5),
                    flierprops=dict(markerfacecolor='red', marker='o', markersize=8, linestyle='none'),
                    medianprops=dict(color='black', linewidth=2))

# Assign colors to each boxplot
for patch, color in zip(bp['boxes'], box_colors):
    patch.set_facecolor(color)

# Add scatter plots and annotate statistics (After Removing Outliers)
for i, season_data in enumerate(seasons_no_outliers):
    jitter = np.random.normal(0, 0.03, len(season_data))
    axs[1].scatter([i + 1 + jitter_offset for jitter_offset in jitter], season_data, color='black', alpha=0.6, s=15)
    mean = np.mean(season_data)
    std = np.std(season_data)
    axs[1].text(i + 1, mean + 0.3, f'Mean: {mean:.2f}', ha='center', va='bottom', color='darkblue', fontsize=12, fontweight='bold')
    axs[1].text(i + 1, mean - 0.3, f'Std: {std:.2f}', ha='center', va='top', color='darkred', fontsize=12, fontweight='bold')

# Add a simple legend to the right of the first plot
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='gold', markersize=10, label='Z-Score Outlier'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, label='IQR Outlier')
]
axs[0].legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10)

# Add gridlines to both plots
for ax in axs:
    ax.grid(True, axis='y', linestyle='--', linewidth=0.7, alpha=0.7)

# Add a caption to the plots
caption = ("Figure: Comparison of temperature distributions across seasons.\n"
           "The left plot shows the original data with Z-Score (gold) and IQR (orange) outliers highlighted.\n"
           "The right plot shows the cleaned data with outliers removed for better representation of seasonal trends.")
plt.figtext(0.5, -0.15, caption, wrap=True, horizontalalignment='center', fontsize=14, color='black')

# Adjust layout for better fit
plt.tight_layout()
plt.show()
