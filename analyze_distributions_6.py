import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import shapiro, skew, kurtosis
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

def load_and_prepare_data(file_path):
    """
    Load the Excel file and preprocess the data.
    - Converts the 'date' column to datetime.
    - Sets 'date' as the index.
    """
    data = pd.read_excel(file_path)
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    return data

def save_figure_with_caption(fig, caption, save_path):
    """
    Save a Matplotlib figure as a PDF with a caption.
    """
    with PdfPages(save_path) as pdf:
        pdf.savefig(fig, bbox_inches='tight')
        plt.figtext(0.5, 0.01, caption, wrap=True, horizontalalignment='center', fontsize=10)
        pdf.close()

def analyze_distributions(data, columns, output_folder=None):
    """
    Analyze and visualize the distribution of specified data columns.
    - Plot histograms and KDEs for each column in subplots.
    - Calculate skewness, kurtosis, and normality test for each column.
    - Save the figure and table as files.
    """
    stats_results = {}
    num_columns = len(columns)
    
    # Prepare subplots
    fig, axs = plt.subplots(num_columns, 1, figsize=(12, 6 * num_columns), sharex=False)
    if num_columns == 1:
        axs = [axs]  # Ensure axs is iterable even for 1 subplot

    # Analyze each column
    for i, column in enumerate(columns):
        col_data = data[column].dropna()
        
        # Calculate skewness, kurtosis, and normality
        col_skewness = skew(col_data)
        col_kurtosis = kurtosis(col_data)
        shapiro_stat, shapiro_p = shapiro(col_data)
        normality = "Yes" if shapiro_p > 0.05 else "No"
        
        # Add results to table
        stats_results[column] = {
            "Skewness": col_skewness,
            "Kurtosis": col_kurtosis,
            "Shapiro-Wilk Test Stat": shapiro_stat,
            "Shapiro-Wilk P-value": shapiro_p,
            "Normal Distribution": normality
        }
        
        # Plot histogram and KDE
        sns.histplot(col_data, bins=30, kde=True, color='skyblue', edgecolor='black', stat="density", ax=axs[i])
        axs[i].set_title(f'Distribution of {column.upper()}', fontsize=16, fontweight='bold')
        axs[i].set_xlabel(f'{column.upper()}', fontsize=14)
        axs[i].set_ylabel('Density', fontsize=14)
        axs[i].grid(True, linestyle='--', alpha=0.6)
    
    plt.tight_layout()
    
    # Save the figure
    if output_folder:
        fig_path = f"{output_folder}/Weather_Distributions.pdf"
        caption = "Figure 1: Distributions of temperature, wind speed, and precipitation with KDE."
        save_figure_with_caption(fig, caption, fig_path)
    plt.show()
    
    # Save and print the table
    stats_table = pd.DataFrame(stats_results).T
    print("\nStatistical Analysis Table:")
    print(stats_table)
    
    if output_folder:
        table_path = f"{output_folder}/Weather_Stats_Table.csv"
        stats_table.to_csv(table_path)
        print(f"Statistical analysis table saved at: {table_path}")

# Specify the path of the Excel file and the output folder
file_path = r'E:\CompAppTools\Project\TehranWeather.xlsx'
output_folder = r'E:\CompAppTools\FinalProject-MH\Final_Project_CMSC6950'

# Load and prepare data
data = load_and_prepare_data(file_path)

# Analyze the distributions of temperature, wind speed, and precipitation
columns_to_analyze = ['tavg', 'wspd', 'prcp']
analyze_distributions(data, columns=columns_to_analyze, output_folder=output_folder)