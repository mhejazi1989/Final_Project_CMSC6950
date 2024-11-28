import matplotlib.pyplot as plt
import seaborn as sns
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

def plot_full_correlation_heatmap(data, output_folder=None):
    """
    Plot and save a heatmap of correlations for selected numerical columns.
    """
    # Focus only on specific columns
    columns_to_include = ['tavg', 'prcp', 'wspd', 'pres']
    numerical_data = data[columns_to_include]
    corr_matrix = numerical_data.corr()

    plt.figure(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, square=True)
    
    plt.title("Correlation Heatmap: Weather Variables", fontsize=16, fontweight="bold")
    plt.xlabel("Variables", fontsize=12)
    plt.ylabel("Variables", fontsize=12)
    
    legend_labels = {
        'tavg': 'Average Temperature (°C)',
        'prcp': 'Precipitation (mm)',
        'wspd': 'Wind Speed (m/s)',
        'pres': 'Atmospheric Pressure (hPa)'
    }

    # Add legend box on the right
    legend_text = "\n".join(f"{k}: {v}" for k, v in legend_labels.items())
    plt.text(1.25, 0.5, legend_text, transform=plt.gca().transAxes, fontsize=10, verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5))

    plt.tight_layout()
    if output_folder:
        heatmap_path = f"{output_folder}/Filtered_Correlation_Heatmap.pdf"
        plt.savefig(heatmap_path, bbox_inches='tight')
        print(f"Filtered correlation heatmap saved at: {heatmap_path}")
    plt.show()

def plot_full_pairplot(data, output_folder=None):
    """
    Plot and save pairplots for selected numerical columns.
    """
    # Focus only on specific columns
    columns_to_include = ['tavg', 'prcp', 'wspd', 'pres']
    numerical_data = data[columns_to_include].dropna()

    pairplot = sns.pairplot(numerical_data, diag_kind="kde", plot_kws={"alpha": 0.7})
    pairplot.fig.suptitle("Pairplot: Weather Variables", y=1.02, fontsize=16, fontweight="bold")
    
    legend_labels = {
        'tavg': 'Average Temperature (°C)',
        'prcp': 'Precipitation (mm)',
        'wspd': 'Wind Speed (m/s)',
        'pres': 'Atmospheric Pressure (hPa)'
    }

    # Add legend box on the right
    legend_text = "\n".join(f"{k}: {v}" for k, v in legend_labels.items())
    pairplot.fig.text(1.05, 0.5, legend_text, fontsize=14, verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5))
    
    if output_folder:
        pairplot_path = f"{output_folder}/Filtered_Pairplot.pdf"
        pairplot.savefig(pairplot_path)
        print(f"Filtered pairplot saved at: {pairplot_path}")
    plt.show()

# Plot the heatmap and pairplot
output_folder = None
plot_full_correlation_heatmap(df, output_folder=output_folder)
plot_full_pairplot(df, output_folder=output_folder)