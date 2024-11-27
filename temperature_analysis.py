import pandas as pd
import matplotlib.pyplot as plt

def load_and_prepare_data(file_path):
    """
    Load the Excel file and preprocess the data.
    - Converts the 'date' column to datetime.
    - Sets 'date' as the index.
    
    Args:
        file_path (str): Path to the Excel file.
    
    Returns:
        pd.DataFrame: Preprocessed DataFrame.
    """
    data = pd.read_excel(file_path)
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    return data

def find_extreme_values(data):
    """
    Find the extreme temperatures and their corresponding dates.
    
    Args:
        data (pd.DataFrame): DataFrame with temperature data.
    
    Returns:
        tuple: (max_temp, max_temp_date, min_temp, min_temp_date)
    """
    max_temp = data['tmax'].max()
    max_temp_date = data['tmax'].idxmax()
    min_temp = data['tmin'].min()
    min_temp_date = data['tmin'].idxmin()
    return max_temp, max_temp_date, min_temp, min_temp_date

def plot_temperature_trends(data, max_temp, max_temp_date, min_temp, min_temp_date, mean_temp, save_path=None):
    """
    Plot temperature trends and highlight extreme values along with mean temperature.
    
    Args:
        data (pd.DataFrame): DataFrame with temperature data.
        max_temp (float): Maximum temperature value.
        max_temp_date (pd.Timestamp): Date of maximum temperature.
        min_temp (float): Minimum temperature value.
        min_temp_date (pd.Timestamp): Date of minimum temperature.
        mean_temp (float): Mean temperature value.
        save_path (str, optional): Path to save the plot as a PDF.
    """
    plt.figure(figsize=(16, 10))
    plt.rcParams.update({
        'font.size': 14,
        'axes.titlesize': 20,
        'axes.labelsize': 16,
        'legend.fontsize': 14,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12
    })

    # Plotting temperatures
    plt.plot(data.index, data['tmin'], label='Min Temperature (°C)', color='blue', linestyle='--', linewidth=2)
    plt.plot(data.index, data['tmax'], label='Max Temperature (°C)', color='red', linestyle='--', linewidth=2)
    plt.plot(data.index, data['tavg'], label='Average Temperature (°C)', color='orange', linewidth=3)
    plt.fill_between(data.index, data['tmin'], data['tmax'], color='lightgray', alpha=0.3)

    # Highlight extreme values
    plt.scatter(max_temp_date, max_temp, color='red', label=f'Highest Max Temp ({max_temp}°C)', s=100, zorder=5)
    plt.scatter(min_temp_date, min_temp, color='blue', label=f'Lowest Min Temp ({min_temp}°C)', s=100, zorder=5)

    # Annotating extreme values outside the plot with a box and arrow
    plt.annotate(
        f'Max Temp: {max_temp}°C', 
        (max_temp_date, max_temp), 
        textcoords="offset points", 
        xytext=(120, 30),  # Position outside the plot
        ha='center', 
        color='red', 
        fontsize=12, 
        fontweight='bold', 
        bbox=dict(facecolor='white', edgecolor='red', boxstyle='round,pad=1'),
        arrowprops=dict(arrowstyle="->", color='red')
    )
    plt.annotate(
        f'Min Temp: {min_temp}°C', 
        (min_temp_date, min_temp), 
        textcoords="offset points", 
        xytext=(-50, -100),  # Position outside the plot
        ha='center', 
        color='blue', 
        fontsize=12, 
        fontweight='bold', 
        bbox=dict(facecolor='white', edgecolor='blue', boxstyle='round,pad=1'),
        arrowprops=dict(arrowstyle="->", color='blue')
    )

    # Adding mean temperature line
    plt.axhline(y=mean_temp, color='green', linestyle='-', linewidth=2, label=f'Mean Temp ({mean_temp:.2f}°C)')

    # Adding labels, title, and legend
    plt.title('Temperature Trends in Tehran Over Time with Extremes Highlighted', fontweight='bold')
    plt.xlabel('Month', fontweight='bold')
    plt.ylabel('Temperature (°C)', fontweight='bold')
    plt.legend(loc='upper left')
    plt.grid()

    # Change x-axis to month names
    plt.xticks(ticks=data.index[::30], labels=data.index.month_name()[::30], rotation=45)

    # Adding a caption
    caption = (
        "This plot illustrates the trends in minimum, maximum, and average temperatures in Tehran over time. "
        "Highlighted are the extreme temperatures: the highest maximum temperature and the lowest minimum temperature, "
        "along with their corresponding dates. Shaded areas between the minimum and maximum temperatures "
        "represent the range of temperature variation on each day. The green horizontal line represents the mean temperature."
    )
    plt.figtext(
        0.5, -0.1, caption, 
        wrap=True, horizontalalignment='center', fontsize=14, color='black'
    )

    plt.tight_layout()

# Main script
file_path = r'E:\CompAppTools\Project\TehranWeather.xlsx'
data = load_and_prepare_data(file_path)
max_temp, max_temp_date, min_temp, min_temp_date = find_extreme_values(data)
mean_temp = data['tavg'].mean()  # Calculate the mean temperature
save_path = r'E:\CompAppTools\FinalProject-MH\Final_Project_CMSC6950\Temp_extreme_Plot.pdf'

# Call the function to plot and save the figure
plot_temperature_trends(data, max_temp, max_temp_date, min_temp, min_temp_date, mean_temp, save_path)

# Save the plot as a PDF if a save_path is provided
if save_path:
        plt.savefig(save_path, format='pdf', bbox_inches='tight')  # Ensure caption is included
        print(f"Plot saved as {save_path}")
    
plt.show()
