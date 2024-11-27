import pytest
import pandas as pd
from unittest.mock import patch
from scipy.stats import skew, kurtosis, shapiro
from analyze_distributions_6 import load_and_prepare_data, analyze_distributions

# Create sample data for testing
sample_data = {
    'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
    'tavg': [20, 21, 22, 23, 24],  # Temperature
    'wspd': [5, 7, 6, 5, 4],  # Wind speed
    'prcp': [0.1, 0.0, 0.2, 0.0, 0.3]  # Precipitation
}

# Convert the sample data into a DataFrame
data = pd.DataFrame(sample_data)
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)


@pytest.mark.parametrize(
    'columns, expected_stats', [
        (
            ['tavg', 'wspd', 'prcp'],
            {
                'tavg': {
                    'Skewness': pytest.approx(skew([20, 21, 22, 23, 24]), rel=1e-2),
                    'Kurtosis': pytest.approx(kurtosis([20, 21, 22, 23, 24]), rel=1e-2),
                    'Shapiro-Wilk Test Stat': pytest.approx(shapiro([20, 21, 22, 23, 24])[0], rel=1e-2),
                    'Shapiro-Wilk P-value': pytest.approx(shapiro([20, 21, 22, 23, 24])[1], rel=1e-2),
                    'Normal Distribution': 'Yes' if shapiro([20, 21, 22, 23, 24])[1] > 0.05 else 'No'
                },
                'wspd': {
                    'Skewness': pytest.approx(skew([5, 7, 6, 5, 4]), rel=1e-2),
                    'Kurtosis': pytest.approx(kurtosis([5, 7, 6, 5, 4]), rel=1e-2),
                    'Shapiro-Wilk Test Stat': pytest.approx(shapiro([5, 7, 6, 5, 4])[0], rel=1e-2),
                    'Shapiro-Wilk P-value': pytest.approx(shapiro([5, 7, 6, 5, 4])[1], rel=1e-2),
                    'Normal Distribution': 'Yes' if shapiro([5, 7, 6, 5, 4])[1] > 0.05 else 'No'
                },
                'prcp': {
                    'Skewness': pytest.approx(skew([0.1, 0.0, 0.2, 0.0, 0.3]), rel=1e-2),
                    'Kurtosis': pytest.approx(kurtosis([0.1, 0.0, 0.2, 0.0, 0.3]), rel=1e-2),
                    'Shapiro-Wilk Test Stat': pytest.approx(shapiro([0.1, 0.0, 0.2, 0.0, 0.3])[0], rel=1e-2),
                    'Shapiro-Wilk P-value': pytest.approx(shapiro([0.1, 0.0, 0.2, 0.0, 0.3])[1], rel=1e-2),
                    'Normal Distribution': 'Yes' if shapiro([0.1, 0.0, 0.2, 0.0, 0.3])[1] > 0.05 else 'No'
                }
            }
        )
    ]
)
def test_analyze_distributions(columns, expected_stats):
    """
    Test the analyze_distributions function.
    - This test checks if the skewness, kurtosis, and normality test results are correct.
    - It also validates the generation of the stats table.
    """

    # Mock the file-saving functions to avoid actual file operations
    with patch('your_module.save_figure_with_caption') as mock_save_figure, \
         patch('matplotlib.pyplot.show') as mock_show, \
         patch('pandas.DataFrame.to_csv') as mock_to_csv:

        # Call the analyze_distributions function
        stats_table = analyze_distributions(data, columns=columns)

        # Assert the statistics for each column
        for column in columns:
            assert stats_table.at[column, 'Skewness'] == expected_stats[column]['Skewness']
            assert stats_table.at[column, 'Kurtosis'] == expected_stats[column]['Kurtosis']
            assert stats_table.at[column, 'Shapiro-Wilk Test Stat'] == expected_stats[column]['Shapiro-Wilk Test Stat']
            assert stats_table.at[column, 'Shapiro-Wilk P-value'] == expected_stats[column]['Shapiro-Wilk P-value']
            assert stats_table.at[column, 'Normal Distribution'] == expected_stats[column]['Normal Distribution']

        # Ensure the save figure function was called (for coverage)
        mock_save_figure.assert_called_once()

        # Ensure the table was saved as a CSV file
        mock_to_csv.assert_called_once()

        # Ensure the show function was called (which implies plot was generated)
        mock_show.assert_called_once()

