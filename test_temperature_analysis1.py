import pytest
import pandas as pd
from unittest.mock import patch
from io import StringIO
from temperature_analysis_1 import load_and_prepare_data, find_extreme_values, plot_temperature_trends

# Sample mock data for testing purposes
mock_data = """
date,tmin,tmax,tavg
2024-01-01,-5,5,0
2024-01-02,-6,6,0
2024-01-03,-7,7,0
2024-01-04,-8,8,0
2024-01-05,-4,4,0
2024-01-06,-3,3,0
"""

# Mocking the loading of Excel data using StringIO (mocked Excel CSV data)
@pytest.fixture
def mock_file():
    return StringIO(mock_data)

# Test for load_and_prepare_data function
@pytest.mark.parametrize("file_path, expected_columns", [
    ("mock_path.xlsx", ["tmin", "tmax", "tavg"])  # Expecting 'tmin', 'tmax', 'tavg' columns
])
@patch('pandas.read_excel')
def test_load_and_prepare_data(mock_read_excel, mock_file, file_path, expected_columns):
    # Mocking the pandas read_excel function to return the mock data
    mock_read_excel.return_value = pd.read_csv(mock_file)
    
    # Call the function with the mocked file path
    data = load_and_prepare_data(file_path)
    
    # Check if the dataframe contains expected columns after loading and processing
    assert set(data.columns) == set(expected_columns)
    assert data.index.name == 'date'  # Checking if 'date' is set as the index

# Test for find_extreme_values function
@pytest.mark.parametrize("data, expected_max, expected_max_date, expected_min, expected_min_date", [
    (pd.read_csv(StringIO(mock_data), parse_dates=["date"], index_col="date"),
     8, pd.Timestamp("2024-01-04"), -8, pd.Timestamp("2024-01-04"))  # max = 8, min = -8
])
def test_find_extreme_values(data, expected_max, expected_max_date, expected_min, expected_min_date):
    max_temp, max_temp_date, min_temp, min_temp_date = find_extreme_values(data)
    
    # Check the extreme values
    assert max_temp == expected_max
    assert max_temp_date == expected_max_date
    assert min_temp == expected_min
    assert min_temp_date == expected_min_date

# Test for mean temperature calculation
@pytest.mark.parametrize("data, expected_mean", [
    (pd.read_csv(StringIO(mock_data), parse_dates=["date"], index_col="date"),
     0.0)  # Average of [0, 0, 0, 0, 0, 0] is 0
])
def test_mean_temperature(data, expected_mean):
    mean_temp = data['tavg'].mean()
    
    # Check the calculated mean temperature
    assert mean_temp == expected_mean