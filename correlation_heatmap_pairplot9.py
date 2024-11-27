def plot_full_correlation_heatmap(data, output_folder=None):
    """
    Plot and save a heatmap of correlations for all numerical columns (excluding snow, wpgt, tsun).
    Add a legend with descriptions for each variable.
    """
    # Select numerical columns excluding 'snow', 'wpgt', 'tsun'
    columns_to_include = ['tavg', 'tmin', 'tmax', 'prcp', 'wdir', 'wspd', 'pres']
    numerical_data = data[columns_to_include]
    
    # Compute the correlation matrix
    corr_matrix = numerical_data.corr()
    
    # Create the heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, square=True)
    
    # Title and labels
    plt.title("Correlation Heatmap: Weather Variables", fontsize=16, fontweight="bold")
    plt.xlabel("Variables", fontsize=12)
    plt.ylabel("Variables", fontsize=12)
    
    # Add a legend for descriptions
    legend_labels = {
        'tavg': 'Average Temperature (°C)',
        'tmin': 'Minimum Temperature (°C)',
        'tmax': 'Maximum Temperature (°C)',
        'prcp': 'Precipitation (mm)',
        'wdir': 'Wind Direction (°)',
        'wspd': 'Wind Speed (m/s)',
        'pres': 'Atmospheric Pressure (hPa)'
    }
    
    # Add the legend box with variable descriptions
    for i, label in enumerate(legend_labels.values()):
        plt.text(0.02, 0.02 + i * 0.05, f'{label}', transform=plt.gca().transAxes, fontsize=12, color='black')

    # Tight layout
    plt.tight_layout()
    
    # Save the figure
    if output_folder:
        heatmap_path = f"{output_folder}/Filtered_Correlation_Heatmap.pdf"
        plt.savefig(heatmap_path, bbox_inches='tight')
        print(f"Filtered correlation heatmap saved at: {heatmap_path}")
    plt.show()


def plot_full_pairplot(data, output_folder=None):
    """
    Plot and save pairplots for all numerical columns (excluding snow, wpgt, tsun).
    Add a legend with descriptions for each variable.
    """
    # Select numerical columns excluding 'snow', 'wpgt', 'tsun'
    columns_to_include = ['tavg', 'tmin', 'tmax', 'prcp', 'wdir', 'wspd', 'pres']
    numerical_data = data[columns_to_include].dropna()

    # Create the pairplot
    pairplot = sns.pairplot(numerical_data, diag_kind="kde", plot_kws={"alpha": 0.7})
    
    # Title
    pairplot.fig.suptitle("Pairplot: Weather Variables", y=1.02, fontsize=16, fontweight="bold")
    
    # Add a legend with descriptions
    legend_labels = {
        'tavg': 'Average Temperature (°C)',
        'tmin': 'Minimum Temperature (°C)',
        'tmax': 'Maximum Temperature (°C)',
        'prcp': 'Precipitation (mm)',
        'wdir': 'Wind Direction (°)',
        'wspd': 'Wind Speed (m/s)',
        'pres': 'Atmospheric Pressure (hPa)'
    }
    
    # Adding text annotations on the pairplot
    for label, description in legend_labels.items():
        pairplot.fig.text(0.02, 0.02 + list(legend_labels.values()).index(description) * 0.05,
                          f'{description}', fontsize=12, color='black', ha='left', va='top')

    # Save the pairplot
    if output_folder:
        pairplot_path = f"{output_folder}/Filtered_Pairplot.pdf"
        pairplot.savefig(pairplot_path)
        print(f"Filtered pairplot saved at: {pairplot_path}")
    plt.show()

# Visualize the full correlation heatmap and pairplot
plot_full_correlation_heatmap(data, output_folder=output_folder)
plot_full_pairplot(data, output_folder=output_folder)
