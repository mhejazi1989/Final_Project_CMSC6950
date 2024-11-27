import pytest
import pandas as pd
from datetime import datetime

# Import the function to test
from temp_threshold_analysis_2 import plot_temperature_and_check_majority

# Sample data to test
sample_data = {
    'date': [
        '2024-01-01', '2024-01-02', '2024-02-01', '2024-02-02', '2024-03-01', '2024-03-02',
        '2024-04-01', '2024-04-02', '2024-05-01', '2024-05-02'
    ],
    'tavg': [20, 22, 30, 29, 25, 26, 18, 19, 21, 23]
}

# Prepare a DataFrame for testing
data = pd.DataFrame(sample_data)
data['date'] = pd.to_datetime(data['date'])  # Convert to datetime
data.set_index('date', inplace=True)


@pytest.mark.parametrize(
    'data, expected_majority, expected_monthly_counts', [
        (
            data,  # DataFrame
            'below',  # Expected majority
            {
                'January': {'days_above': 1, 'days_below': 0, 'total_days': 2, 'trend': 'above'},
                'February': {'days_above': 1, 'days_below': 0, 'total_days': 2, 'trend': 'above'},
                'March': {'days_above': 1, 'days_below': 0, 'total_days': 2, 'trend': 'above'},
                'April': {'days_above': 0, 'days_below': 2, 'total_days': 2, 'trend': 'below'},
                'May': {'days_above': 1, 'days_below': 0, 'total_days': 2, 'trend': 'above'}
            }  # Expected monthly breakdown
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

    # Call the function and capture the result
    result = plot_temperature_and_check_majority(data, temp_column='tavg', save_path=None)

    # Extract the majority result from the output
    majority_result = result.split('\n')[0].split(' ')[-2]

    # Assert that the majority trend matches the expected result
    assert majority_result == expected_majority, f"Expected majority trend: {expected_majority}, but got {majority_result}"

    # Extract monthly counts from the printed output (if required, or you can modify to return them directly)
    monthly_trends_output = result.split('\n')[2:]  # Extract the lines containing monthly trends
    monthly_trends = {line.split()[0]: {
        'days_above': int(line.split()[1]),
        'days_below': int(line.split()[3]),
        'total_days': int(line.split()[5]),
        'trend': line.split()[7]
    } for line in monthly_trends_output}

    # Assert that the monthly trends match the expected values
    for month, expected_counts in expected_monthly_counts.items():
        assert monthly_trends.get(month, None) == expected_counts, f"Expected counts for {month}: {expected_counts}, but got {monthly_trends.get(month, None)}"

