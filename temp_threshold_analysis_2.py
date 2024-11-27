import pandas as pd
import matplotlib.pyplot as plt

def plot_temperature_and_check_majority(data, temp_column='tavg', save_path=None):
    """
    Plot days where the temperature is above or below the historical mean by ±1.5 standard deviations,
    determine if the majority of days are above or below the mean ±1.5 SD, and analyze trends by month.
    Also saves the results in a nice table format in a PDF.

    Args:
        data (pd.DataFrame): DataFrame containing temperature data.
        temp_column (str): Column to calculate the mean temperature (default 'tavg').
        save_path (str): Optional path to save the figure as a PDF.
    
    Returns:
        str: A summary of the majority trend and monthly breakdown.
    """
    # Ensure the temperature column exists
    if temp_column not in data.columns:
        raise ValueError(f"The specified temperature column '{temp_column}' does not exist in the DataFrame.")

    # Calculate the historical mean and standard deviation
    historical_mean = data[temp_column].mean()
    historical_std = data[temp_column].std()
    
    # Define thresholds for ±1.5 SD
    upper_threshold = historical_mean + 1.5 * historical_std
    lower_threshold = historical_mean - 1.5 * historical_std

    # Create masks for categories
    above_significant = data[temp_column] > upper_threshold
    below_significant = data[temp_column] < lower_threshold
    normal = ~above_significant & ~below_significant  # Days within ±1.5 std deviation

    # Add month information
    data['month'] = data.index.month
    data['month_name'] = data.index.month_name()

    # Count days by month
    monthly_counts = data.groupby('month').apply(
        lambda x: pd.Series({
            'days_above': (x[temp_column] > upper_threshold).sum(),
            'days_below': (x[temp_column] < lower_threshold).sum(),
        })
    )
    monthly_counts['total_days'] = monthly_counts['days_above'] + monthly_counts['days_below']
    monthly_counts['trend'] = monthly_counts.apply(
        lambda x: 'above' if x['days_above'] > x['days_below'] else 'below', axis=1
    )

    # Print monthly trends with month names
    monthly_counts.index = monthly_counts.index.map(lambda x: pd.to_datetime(f'2024-{x:02d}-01').strftime('%B'))  # Convert month numbers to names
    print(monthly_counts)

    # Determine majority category overall
    count_above = above_significant.sum()
    count_below = below_significant.sum()
    count_normal = normal.sum()
    majority = "above" if count_above > count_below else "below" if count_below > count_above else "equal"

    print(f"Days above +1.5 SD: {count_above}")
    print(f"Days below -1.5 SD: {count_below}")
    print(f"Days within ±1.5 SD: {count_normal}")
    print(f"The majority of days are {majority} the ±1.5 SD threshold.")

    # Plot the results
    plt.figure(figsize=(14, 8))
    plt.scatter(data.index[above_significant], data[temp_column][above_significant], 
                color='green', label='Above Mean + 1.5 Std', alpha=0.7, s=50)
    plt.scatter(data.index[below_significant], data[temp_column][below_significant], 
                color='red', label='Below Mean - 1.5 Std', alpha=0.7, s=50)
    plt.scatter(data.index[normal], data[temp_column][normal], 
                color='blue', label='Within ±1.5 Std', alpha=0.5, s=30)
    plt.axhline(y=historical_mean, color='black', linestyle='--', label='Mean Temperature', linewidth=1.5)
    plt.title(r"$\mathbf{Days\ Above/Below\ \pm1.5\ Std\ Dev\ from\ Historical\ Mean\ Temperature}$", fontsize=16)
    plt.xlabel('Date (Month)', fontsize=14)
    plt.ylabel('Temperature (°C)', fontsize=14)

    # Set x-axis as month names
    plt.xticks(data.index[::30], data['month_name'][::30], rotation=45)  # Adjust ticks for clarity

    plt.legend(loc='best', fontsize=12)
    plt.grid(True)

  # Add a caption to the plot
    caption = (
        "This plot illustrates the temperature trends over time, showing days where the temperature is "
        "above or below the historical mean by ±1.5 standard deviations. The green dots represent days with "
        "temperatures above the mean +1.5 standard deviations, the red dots represent days below the mean -1.5 "
        "standard deviations, and the blue dots represent days within the ±1.5 standard deviation range."
    )
    plt.figtext(0.5, -0.15, caption, wrap=True, horizontalalignment='center', fontsize=14, color='black')

    # Save the plot as a PDF if save_path is provided
    if save_path:
        plt.savefig(save_path, format='pdf')
        print(f"Plot saved to {save_path}")

    # Show the plot
    plt.show()

    # Create and save the results as a table
    fig, ax = plt.subplots(figsize=(5.5, 3.5))  # Create a new figure for the table
    ax.axis('off')  # Hide the axis

    # Convert the DataFrame to a table and style it
    table_data = monthly_counts.reset_index()
    table = plt.table(cellText=table_data.values, colLabels=table_data.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)  # Adjust the table size
    
    # Add a title to the table
    fig.text(0.5, 0.95, 'Table 1: Monthly Trends in Temperature Above/Below ±1.5 Std', 
         ha='center', va='top', fontsize=14, fontweight='bold')

   # Tighten layout to reduce excess space
    plt.subplots_adjust(left=0.1, right=0.9, top=0.8, bottom=0.1)


    # Save the table as a PDF
    table_pdf_path = save_path.replace(".pdf", "_Table.pdf")
    plt.savefig(table_pdf_path, format='pdf')
    print(f"Table saved to {table_pdf_path}")
   

    # Return the majority result and monthly breakdown
    return f"The majority of days are {majority} the ±1.5 SD threshold.\n\nMonthly Trends:\n{monthly_counts}"

# Example usage
file_path = r'E:\CompAppTools\Project\TehranWeather.xlsx'  # Replace with your file path
data = pd.read_excel(file_path)
data['date'] = pd.to_datetime(data['date'])  # Convert the date column to datetime format
data.set_index('date', inplace=True)

# Call the function
save_path = r'E:\CompAppTools\FinalProject-MH\Final_Project_CMSC6950\Temperature_Above_Below_Mean_Plot_with_1_5Std.pdf'
result = plot_temperature_and_check_majority(data, temp_column='tavg', save_path=save_path)
print(result)

