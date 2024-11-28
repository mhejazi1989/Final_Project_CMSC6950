import pytest
import numpy as np
import pandas as pd
from detect_outliers_3 import detect_outliers  # Import the function to be tested

# Sample data for testing
test_data = {
    'Winter': [15, 20, 22, 30, 25, 19, 21, 16, 23, 18],  # No outliers
    'Spring': [10, 12, 13, 15, 11, 14, 10, 9, 8, 7],  # No outliers
    'Summer': [30, 35, 33, 40, 38, 36, 37, 35, 39, 42],  # No outliers
    'Fall': [5, 7, 6, 4, 5, 6, 7, 9, 8, 12]  # Outlier 12
}

# Parametrize the test data
@pytest.mark.parametrize("season, data, expected_z_outliers, expected_iqr_outliers", [
    ('Winter', [15, 20, 22, 30, 25, 19, 21, 16, 23, 18], [], []),  # No outliers
    ('Spring', [10, 12, 13, 15, 11, 14, 10, 9, 8, 7], [], []),  # No outliers
    ('Summer', [30, 35, 33, 40, 38, 36, 37, 35, 39, 42], [], []),  # No outliers
    ('Fall', [5, 7, 6, 4, 5, 6, 7, 9, 8, 12], [12], [12]),  # Outlier 12
])
def test_outliers(season, data, expected_z_outliers, expected_iqr_outliers):
    # Call the detect_outliers function with test data
    z_outliers, iqr_outliers, mean, std = detect_outliers(data)
    
    # Assert Z-Score outliers
    assert np.all(np.isin(z_outliers, expected_z_outliers)), f"Failed for Z-Score outliers in {season}"
    
    # Assert IQR outliers
    assert np.all(np.isin(iqr_outliers, expected_iqr_outliers)), f"Failed for IQR outliers in {season}"

# Test the data cleaning process (removing outliers)
def test_remove_outliers():
    # Test data
    season_data = pd.Series([15, 20, 22, 30, 25, 19, 21, 16, 23, 18])
    
    # Detect outliers
    z_outliers, iqr_outliers, mean, std = detect_outliers(season_data)
    
    # Remove the outliers
    clean_data = season_data[~season_data.isin(z_outliers) & ~season_data.isin(iqr_outliers)]
    
    # Ensure the clean data does not contain the outliers
    assert len(clean_data) == len(season_data) - len(z_outliers) - len(iqr_outliers), "Outliers were not removed correctly"

# Test the percentage of outliers removed (ensuring the total removed data is calculated properly)
def test_percentage_outliers_removed():
    seasons_data = [
        pd.Series([15, 20, 22, 30, 25, 19, 21, 16, 23, 18]),  # Winter
        pd.Series([10, 12, 13, 15, 11, 14, 10, 9, 8, 7]),  # Spring
        pd.Series([30, 35, 33, 40, 38, 36, 37, 35, 39, 42]),  # Summer
        pd.Series([5, 7, 6, 4, 5, 6, 7, 9, 8, 12])  # Fall
    ]
    
    total_removed = 0
    total_data_points = 0
    
    # Loop through the seasons
    for season_data in seasons_data:
        z_outliers, iqr_outliers, _, _ = detect_outliers(season_data)
        
        # Clean the data
        clean_data = season_data[~season_data.isin(z_outliers) & ~season_data.isin(iqr_outliers)]
        
        # Track removed data
        removed_data = len(season_data) - len(clean_data)
        total_removed += removed_data
        total_data_points += len(season_data)
    
    # Calculate the total percentage of data removed
    percentage_removed = (total_removed / total_data_points) * 100
    assert percentage_removed < 10, f"Total outlier removal is too high: {percentage_removed}%"
