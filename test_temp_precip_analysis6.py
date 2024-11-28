import pytest
import pandas as pd
from datetime import datetime

# Import the function you want to test
from temp_precip_analysis_6 import load_and_prepare_data, plot_temperature_and_precipitation

# Sample data for testing (mock data)
@pytest.fixture
def mock_data():
    data = {
        'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
        'tmax': [15, 16, 14, 17, 19],
        'tmin': [5, 6, 4, 7, 6],
        'tavg': [10, 11, 9, 12, 12],
        'prcp': [1.2, 0.0, 3.4, 0.0, 0.5]
    }
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df

# Test for load_and_prepare_data function
def test_load_and_prepare_data(mock_data):
    # Save the mock data to a file and reload it
    file_path = 'mock_data.xlsx'
    mock_data.to_excel(file_path)
    
    # Load data using the function
    loaded_data = load_and_prepare_data(file_path)
    
    # Check if the index is set to 'date' and is datetime
    assert isinstance(loaded_data.index, pd.DatetimeIndex)
    assert all(loaded_data.index == mock_data.index)
    
    # Check if the columns are the same
    assert list(loaded_data.columns) == ['tmax', 'tmin', 'tavg', 'prcp']

# Test for plot_temperature_and_precipitation function
@pytest.mark.parametrize(
    "data, expected_max_temp, expected_min_temp, expected_correlation",
    [
        (
            pd.DataFrame({
                'tmax': [20, 22, 19, 21],
                'tmin': [10, 12, 11, 13],
                'tavg': [15, 17, 16, 17],
                'prcp': [0, 1.2, 0, 3.4],
                'date': pd.date_range(start="2023-01-01", periods=4)
            }).set_index('date'),
            22, 10, 0.48  # Updated expected correlation value
        )
    ]
)
def test_plot_temperature_and_precipitation(data, expected_max_temp, expected_min_temp, expected_correlation):
    # Extreme value testing
    max_temp = data['tmax'].max()
    min_temp = data['tmin'].min()
    
    assert max_temp == expected_max_temp
    assert min_temp == expected_min_temp

    # Correlation testing
    temp_precip_correlation = data[['tavg', 'prcp']].corr().iloc[0, 1]
    assert abs(temp_precip_correlation - expected_correlation) < 0.1  # Allowing small tolerance

    # Check for months with less than the mean precipitation
    mean_precip = data['prcp'].mean()
    months_below_mean = data[data['prcp'] < mean_precip].index.strftime('%b')
    assert 'Jan' in months_below_mean  # Modify this check based on your test data and expected output
