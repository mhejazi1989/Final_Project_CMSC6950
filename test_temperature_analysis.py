import pytest
import pandas as pd
import os
from io import StringIO
import matplotlib.pyplot as plt
from matplotlib.testing.compare import compare_images
from temperature_analysis import load_and_prepare_data, find_extreme_values, plot_temperature_trends

# Sample data for testing
@pytest.fixture
def sample_data():
    data = """
    date,tmax,tmin,tavg
    2024-01-01,15,5,10
    2024-01-02,17,6,11.5
    2024-01-03,20,8,14
    2024-01-04,13,4,8.5
    2024-01-05,18,7,12.5
    2024-01-06,19,6,12.5
    """
    return pd.read_csv(StringIO(data), parse_dates=["date"])

# Test loading and preparing data
def test_load_and_prepare_data(sample_data):
    file_path = "test_data.csv"
    sample_data.to_csv(file_path, index=False)
    
    df = load_and_prepare_data(file_path)
    
    # Check if the data is loaded and the index is set correctly
    assert isinstance(df, pd.DataFrame)
    assert df.index.name == 'date'
    assert df.shape[0] == 6  # We have 6 rows in the sample data
    os.remove(file_path)  # Clean up the test file

# Test finding extreme values
@pytest.mark.parametrize(
    "max_temp, max_temp_date, min_temp, min_temp_date",
    [(20, "2024-01-03", 4, "2024-01-04")]
)
def test_find_extreme_values(sample_data, max_temp, max_temp_date, min_temp, min_temp_date):
    max_temp_val, max_temp_date_val, min_temp_val, min_temp_date_val = find_extreme_values(sample_data)
    
    # Check if the extreme values match the expected values
    assert max_temp_val == max_temp
    assert max_temp_date_val.strftime('%Y-%m-%d') == max_temp_date
    assert min_temp_val == min_temp
    assert min_temp_date_val.strftime('%Y-%m-%d') == min_temp_date

# Test plotting the temperature trends
@pytest.mark.parametrize("save_path", ["test_plot.pdf"])
def test_plot_temperature_trends(sample_data, save_path):
    max_temp, max_temp_date, min_temp, min_temp_date = find_extreme_values(sample_data)
    
    # Check if the plot function runs without error
    try:
        plot_temperature_trends(sample_data, max_temp, max_temp_date, min_temp, min_temp_date, save_path)
    except Exception as e:
        pytest.fail(f"Plotting failed with error: {e}")
    
    # Check if the plot is saved successfully
    assert os.path.exists(save_path)  # Ensure the plot is saved as a PDF
    os.remove(save_path)  # Clean up the test plot file

# Test comparing the generated plot with an expected plot (useful if you have a reference plot)
def test_compare_plot():
    # Generate plot and save as a temporary file
    expected_path = "expected_plot.png"
    generated_path = "generated_plot.png"

    # Assuming the sample data is loaded here again
    data = """
    date,tmax,tmin,tavg
    2024-01-01,15,5,10
    2024-01-02,17,6,11.5
    2024-01-03,20,8,14
    2024-01-04,13,4,8.5
    2024-01-05,18,7,12.5
    2024-01-06,19,6,12.5
    """
    df = pd.read_csv(StringIO(data), parse_dates=["date"])

    max_temp, max_temp_date, min_temp, min_temp_date = find_extreme_values(df)

    # Save the expected plot
    plot_temperature_trends(df, max_temp, max_temp_date, min_temp, min_temp_date, expected_path)

    # Create a new plot to compare
    plot_temperature_trends(df, max_temp, max_temp_date, min_temp, min_temp_date, generated_path)

    # Compare the images
    result = compare_images(expected_path, generated_path, tol=5e-2)
    
    assert result is None, f"Plots do not match: {result}"

    # Clean up the test plots
    os.remove(expected_path)
    os.remove(generated_path)

