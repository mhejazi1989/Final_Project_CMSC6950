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

def plot_temperature_and_precipitation(data, save_path=None):
    """
    Plot temperature trends (avg, min, max) and precipitation on the same graph.
    - Temperature will be in light colors.
    - Precipitation will be darker (dark purple) and with thicker bars.
    Also identifies and highlights extreme values (max/min temperature and precipitation).
    - Computes and displays the correlation between temperature and precipitation.
    - Displays months with less than the mean precipitation.
    
    Args:
        data (pd.DataFrame): DataFrame containing temperature and precipitation data.
        save_path (str): Optional path to save the figure as a PDF.
    """
    
    # Find extreme values (max/min for temperature and precipitation)
    max_temp = data['tmax'].max()
    max_temp_date = data['tmax'].idxmax()
    min_temp = data['tmin'].min()
    min_temp_date = data['tmin'].idxmin()
    
    max_precip = data['prcp'].max()
    max_precip_date = data['prcp'].idxmax()
    min_precip = data['prcp'].min()
    min_precip_date = data['prcp'].idxmin()

    # Calculate monthly mean precipitation
    monthly_precip = data['prcp'].resample('M').mean()
    
    # Calculate overall mean precipitation
    mean_precip = data['prcp'].mean()
    
    # Identify months with less than the mean precipitation
    months_below_mean = monthly_precip[monthly_precip < mean_precip].index.strftime('%b')

    # Calculate correlation between temperature and precipitation
    temp_precip_correlation = data[['tavg', 'prcp']].corr().iloc[0, 1]
    
    # Create the plot with a larger figure size
    fig, ax1 = plt.subplots(figsize=(20, 12))  # Bigger figure size
    
    # Plot temperature trends with light colors
    ax1.plot(data.index, data['tmin'], label='Min Temperature (°C)', color='lightblue', linestyle='--', linewidth=2)
    ax1.plot(data.index, data['tmax'], label='Max Temperature (°C)', color='lightcoral', linestyle='--', linewidth=2)
    ax1.plot(data.index, data['tavg'], label='Average Temperature (°C)', color='lightgreen', linewidth=3)
    ax1.set_xlabel('Date', fontsize=18)
    ax1.set_ylabel('Temperature (°C)', color='black', fontsize=18)
    ax1.tick_params(axis='y', labelcolor='black', labelsize=16)
    
    # Create a second y-axis for precipitation with dark purple color and thicker bars
    ax2 = ax1.twinx()
    ax2.bar(data.index, data['prcp'], color='purple', alpha=0.8, width=1.0, label='Precipitation (mm)', linewidth=2)
    ax2.set_ylabel('Precipitation (mm)', color='blue', fontsize=18)
    ax2.tick_params(axis='y', labelcolor='blue', labelsize=16)
    
    # Highlight extreme values on the plot
    ax1.scatter(max_temp_date, max_temp, color='lightgray', label=f'Highest Max Temp ({max_temp}°C)', s=150, zorder=5)
    ax1.scatter(min_temp_date, min_temp, color='lightgray', label=f'Lowest Min Temp ({min_temp}°C)', s=150, zorder=5)
    ax2.scatter(max_precip_date, max_precip, color='darkgreen', label=f'Highest Precip ({max_precip}mm)', s=200, zorder=5, edgecolor='black', linewidth=2)
    ax2.scatter(min_precip_date, min_precip, color='purple', label=f'Lowest Precip ({min_precip}mm)', s=200, zorder=5, edgecolor='black', linewidth=2)

    # Annotate extreme values with bold text for precipitation and light color for temperature
    ax1.annotate(f'{max_temp}°C', (max_temp_date, max_temp), textcoords="offset points", xytext=(-100, 30), ha='center', color='lightgray', fontsize=20, fontweight='normal', arrowprops=dict(arrowstyle="->", color='lightgray'))
    ax1.annotate(f'{min_temp}°C', (min_temp_date, min_temp), textcoords="offset points", xytext=(100, -50), ha='center', color='lightgray', fontsize=20, fontweight='normal', arrowprops=dict(arrowstyle="->", color='lightgray'))
    ax2.annotate(f'{max_precip}mm', (max_precip_date, max_precip), textcoords="offset points", xytext=(-100, 20), ha='center', color='darkgreen', fontsize=20, fontweight='bold', arrowprops=dict(arrowstyle="->", color='darkgreen'))
    ax2.annotate(f'{min_precip}mm', (min_precip_date, min_precip), textcoords="offset points", xytext=(100, -50), ha='center', color='purple', fontsize=20, fontweight='bold', arrowprops=dict(arrowstyle="->", color='purple'))

    # Add a horizontal line for the mean precipitation (dark red with thick line)
    ax2.axhline(y=mean_precip, color='darkred', linestyle='-', linewidth=4, label=f'Mean Precipitation ({mean_precip:.2f} mm)')
    
    # Add title and grid
    plt.title('Temperature and Precipitation Trends in Tehran Over Time', fontsize=24, fontweight='bold')
    plt.grid(True)
    
    # Move the legends outside the plot further right
    ax1.legend(loc='upper left', bbox_to_anchor=(1.1, 1), fontsize=16)
    ax2.legend(loc='upper left', bbox_to_anchor=(1.1, 0.7), fontsize=16)

    # Format X-axis to show month names
    ax1.set_xticks(data.index[::int(len(data)/12)])  # Show 12 ticks, approximately one per month
    ax1.set_xticklabels(data.index.strftime('%b')[::int(len(data)/12)], rotation=45, fontsize=16)
    
    # Display correlation in the top-left of the plot
    plt.figtext(0.05, 0.8, f'Temperature-Precipitation Correlation: {temp_precip_correlation:.2f}', fontsize=20, color='black', ha='left')
    
    # Adding the caption to the figure
    caption = (
        "This plot illustrates the trends in minimum, maximum, and average temperatures in Tehran over time. "
        "Temperature trends are shown in light colors, while precipitation is represented with darker purple bars. "
        "Extreme values for both temperature and precipitation are highlighted, and the correlation between "
        "temperature and precipitation is displayed in the top left corner."
    )
    plt.figtext(0.5, -0.05, caption, wrap=True, horizontalalignment='center', fontsize=14, color='black')
    
    # Adjust layout to fit everything properly
    plt.tight_layout()
    
    # Save the figure as a PDF if save_path is provided
    if save_path:
        plt.savefig(save_path, format='pdf')

    # Show the plot
    plt.show()
    
    # Print months with less than mean precipitation
    print("Months with less than the mean precipitation:")
    print(list(months_below_mean))

# Call the function to plot the combined temperature and precipitation data
save_path = r'E:\CompAppTools\FinalProject-MH\Final_Project_CMSC6950\Temp_Precip_Plot_with_Mean.pdf'  
plot_temperature_and_precipitation(data, save_path)
