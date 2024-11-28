import pytest
import pandas as pd
import os
import matplotlib.pyplot as plt
from temp_precip_analysis_5 import load_and_prepare_data, plot_temperature_and_precipitation

@pytest.mark.parametrize("file_path,expected_columns", [
    (r'E:\CompAppTools\Project\TehranWeather.xlsx', ['tavg', 'prcp', 'wspd']),
])
def test_load_and_prepare_data(file_path, expected_columns):
    """
    Test the load_and_prepare_data function to ensure it loads and preprocesses data correctly.
    """
    data = load_and_prepare_data(file_path)
    
    # Ensure that 'date' is the index
    assert isinstance(data.index, pd.DatetimeIndex), "'date' column should be in datetime format"
    
    # Ensure the expected columns are in the dataset
    for column in expected_columns:
        assert column in data.columns, f"Column '{column}' not found in the dataset"

@pytest.mark.parametrize("file_path,output_folder", [
    (r'E:\CompAppTools\Project\TehranWeather.xlsx', r'E:\CompAppTools\FinalProject-MH\Final_Project_CMSC6950'),
])
def test_save_figure_with_caption(file_path, output_folder):
    """
    Test the save_figure_with_caption function to ensure the figure is saved with a caption.
    """
    data = load_and_prepare_data(file_path)
    columns_to_analyze = ['tavg', 'prcp', 'wspd']
    
    # Create figure and save it
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data[columns_to_analyze[0]], label=columns_to_analyze[0])  # Example plot
    caption = "Figure: Test caption"
    fig_path = os.path.join(output_folder, "test_figure.pdf")
    save_figure_with_caption(fig, caption, fig_path)
    
    # Ensure the figure file was created
    assert os.path.exists(fig_path), f"Figure was not saved at {fig_path}"
    
    # Clean up the file after test
    os.remove(fig_path)

@pytest.mark.parametrize("file_path,output_folder", [
    (r'E:\CompAppTools\Project\TehranWeather.xlsx', r'E:\CompAppTools\FinalProject-MH\Final_Project_CMSC6950'),
])
def test_analyze_distributions(file_path, output_folder):
    """
    Test the analyze_distributions function to ensure statistical analysis and plot saving work.
    """
    data = load_and_prepare_data(file_path)
    columns_to_analyze = ['tavg', 'prcp', 'wspd']
    
    # Run the distribution analysis
    analyze_distributions(data, columns=columns_to_analyze, output_folder=output_folder)
    
    # Check if the statistical table CSV is saved
    table_path = os.path.join(output_folder, "Weather_Stats_Table.csv")
    assert os.path.exists(table_path), f"Statistical analysis table was not saved at {table_path}"
    
    # Check if the figure is saved (as done in test_save_figure_with_caption)
    fig_path = os.path.join(output_folder, "Weather_Distributions.pdf")
    assert os.path.exists(fig_path), f"Distribution figure was not saved at {fig_path}"
    
    # Clean up the table and figure files after test
    os.remove(table_path)
    os.remove(fig_path)
