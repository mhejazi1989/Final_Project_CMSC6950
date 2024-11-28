import pytest
import pandas as pd
from unittest import mock
from temp_threshold_analysis_2 import plot_temperature_and_check_majority

# Sample data for testing
sample_data = {
    'date': [
        '2024-01-01', '2024-01-02', '2024-02-01', '2024-02-02', '2024-03-01', '2024-03-02',
        '2024-04-01', '2024-04-02', '2024-05-01', '2024-05-02'
    ],
    'tavg': [20, 22, 30, 29, 25, 26, 18, 19, 21, 23]
}

# Prepare the DataFrame for testing
data = pd.DataFrame(sample_data)
data['date'] = pd.to_datetime(data['date'])  # Convert to datetime
data.set_index('date', inplace=True)

# Expected output for the majority trend and monthly breakdown
expected_majority = 'above'
expected_monthly_counts = {
    'January': {'days_above': 1, 'days_below': 0, 'total_days': 2, 'trend': 'above'},
    'February': {'days_above': 1, 'days_below': 0, 'total_days': 2, 'trend': 'above'},
    'March': {'days_above': 1, 'days_below': 0, 'total_days': 2, 'trend': 'above'},
    'April': {'days_above': 0, 'days_below': 2, 'total_days': 2, 'trend': 'below'},
    'May': {'days_above': 1, 'days_below': 0, 'total_days': 2, 'trend': 'above'}
}

# Test function
@pytest.mark.parametrize(
    'data, expected_majority, expected_monthly_counts', [
        (
            data,  # DataFrame
            expected_majority,  # Expected majority
            expected_monthly_counts  # Expected monthly breakdown
        ),
    ]
)
def test_temperature_analysis(data, expected_majority, expected_monthly_counts):
    """
    Test the temperature analysis function.

    This test checks:
    1. The majority trend (above/below) based on temperature data.
    2. The monthly breakdown for days above and below ±1.5 standard deviations from the mean.
    """

    # Mock the matplotlib methods to prevent plotting during tests
    with mock.patch('matplotlib.pyplot.show'), mock.patch('matplotlib.pyplot.savefig'):
        result = plot_temperature_and_check_majority(data, temp_column='tavg', save_path=None)

    # Check the majority trend in the result
    majority_result = result.split('\n')[0].split(' ')[-2]
    assert majority_result == expected_majority, f"Expected: {expected_majority}, Got: {majority_result}"

    # Extract and check the monthly trends
    monthly_trends_output = result.split('\n')[2:]  # Extract lines with monthly trends
    monthly_trends = {line.split()[0]: {
        'days_above': int(line.split()[1]),
        'days_below': int(line.split()[3]),
        'total_days': int(line.split()[5]),
        'trend': line.split()[7]
    } for line in monthly_trends_output}

    for month, expected_counts in expected_monthly_counts.items():
        assert monthly_trends.get(month, None) == expected_counts, \
            f"Expected for {month}: {expected_counts}, Got: {monthly_trends.get(month, None)}"
