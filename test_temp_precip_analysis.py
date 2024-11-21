import pytest
import pandas as pd
from temp_precip_analysis import load_and_prepare_data, plot_temperature_and_precipitation
import os

# Sample test data for loading and preparing data
@pytest.mark.parametrize("file_path, expected_shape", [
    ("test_data.xlsx", (365, 5)),  # Assuming the file has 365 rows and 5 columns
])
def test_load_and_prepare_data(file_path, expected_shape):
    """
    Test the load_and_prepare_data function to ensure it loads and preprocesses data correctly.
    """
    # Load the test data
    data = load_and_prepare_data(file_path)
    
    # Assert the data shape is as expected
    assert data.shape == expected_shape, f"Expected shape {expected_shape}, but got {data.shape}"
    
    # Ensure that the 'date' column is now the index
    assert isinstance(data.index, pd.DatetimeIndex), "Index should be of type 'DatetimeIndex'"
    
    # Ensure the 'date' column is correctly parsed as datetime
    assert pd.api.types.is_datetime64_any_dtype(data.index), "'date' column should be in datetime format"

# Test the plot function (for this example, we can check if the file is being saved correctly)
@pytest.mark.parametrize("save_path", [
    ("test_plot.pdf"),  # A path to save the plot
])
def test_plot_temperature_and_precipitation(save_path):
    """
    Test the plot_temperature_and_precipitation function to ensure the plot is being generated.
    """
    # Generate sample data
    data = pd.DataFrame({
        'date': pd.date_range(start='2020-01-01', periods=365, freq='D'),
        'tmin': [10] * 365,
        'tmax': [20] * 365,
        'tavg': [15] * 365,
        'prcp': [5] * 365
    })
    
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    
    # Call the function to generate the plot
    plot_temperature_and_precipitation(data, save_path)
    
    # Assert the file is created
    assert os.path.exists(save_path), f"Plot file was not saved at {save_path}"
    
    # Clean up after test
    os.remove(save_path)

