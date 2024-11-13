# Testing Missing Values
import pytest
import pandas as pd

# Sample dataset for testing
sample_data = {
    'date': ['2023-10-01', '2023-10-02', '2023-10-03', None],
    'tavg': [23.1, 23.4, None, 19.7],
    'tmin': [18.7, 18.5, 18.8, None],
    'tmax': [27.3, None, 28.1, 25.3],
}

# Convert to DataFrame
df = pd.DataFrame(sample_data)

@pytest.mark.parametrize("column, expected_missing", [
    ('date', 1),
    ('tavg', 1),
    ('tmin', 1),
    ('tmax', 1),
])
def test_check_missing_values(column, expected_missing):
    assert df[column].isnull().sum() == expected_missing


# Testing Summary Statistics Calculation
@pytest.mark.parametrize("column, expected_mean, expected_min, expected_max", [
    ('tavg', 22.07, 19.7, 23.4),
    ('tmin', 18.67, 18.5, 18.8),
    ('tmax', 26.9, 25.3, 28.1),
])
def test_calculate_summary_statistics(column, expected_mean, expected_min, expected_max):
    mean = df[column].mean()
    min_val = df[column].min()
    max_val = df[column].max()
    
    assert round(mean, 2) == expected_mean
    assert round(min_val, 2) == expected_min
    assert round(max_val, 2) == expected_max

# Testing Z-Score Outlier Detection
import numpy as np
from scipy.stats import zscore

# Sample data including an outlier
sample_data = {
    'tavg': [23.1, 23.4, 100.0, 19.7],  # 100.0 is an extreme outlier
}
df = pd.DataFrame(sample_data)

@pytest.mark.parametrize("column, threshold, expected_outliers", [
    ('tavg', 2, [100.0]),
])
def test_detect_outliers_zscore(column, threshold, expected_outliers):
    df['z_score'] = zscore(df[column])
    outliers = df[column][abs(df['z_score']) > threshold].tolist()
    
    assert outliers == expected_outliers


# Testing IQR Outlier Detection
@pytest.mark.parametrize("column, expected_outliers", [
    ('tavg', [100.0]),
])
def test_detect_outliers_iqr(column, expected_outliers):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[column][(df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR))].tolist()
    
    assert outliers == expected_outliers

# Testing Seasonal Statistics Calculation
# Example function to simulate seasonal data
sample_data['season'] = ['Fall', 'Fall', 'Winter', 'Winter']
df = pd.DataFrame(sample_data)

@pytest.mark.parametrize("season, expected_mean_tavg, expected_mean_prcp", [
    ('Fall', 23.25, 0.0),
    ('Winter', 59.85, 0.0),
])
def test_calculate_seasonal_stats(season, expected_mean_tavg, expected_mean_prcp):
    season_data = df[df['season'] == season]
    mean_tavg = season_data['tavg'].mean()
    
    assert round(mean_tavg, 2) == expected_mean_tavg
