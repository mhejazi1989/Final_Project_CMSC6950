import pytest
import pandas as pd
import numpy as np

@pytest.fixture
def sample_df():
    data = {
        'date': pd.date_range(start='2023-12-01', periods=10, freq='D'),
        'tavg': [15, 16, 17, 20, 21, 22, 23, 24, 25, 26],
        'prcp': [0, 0, 0.5, 1, 0, 2, 3, 0.5, 1, 1],
        'wspd': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    }
    return pd.DataFrame(data)

@pytest.mark.parametrize("season, expected_min_temp, expected_max_temp, expected_mean_temp", [
    ('Winter', 15, 26, 20.9),  # Updated mean temperature
    ('Spring', np.nan, np.nan, np.nan),  # No data
])

def test_seasonal_statistics(sample_df, season, expected_min_temp, expected_max_temp, expected_mean_temp):
    df = sample_df
    df['date'] = pd.to_datetime(df['date'])

    # Adjusted date ranges to match the sample dataset
    winter = (df['date'] >= '2023-12-01') & (df['date'] <= '2023-12-10')
    spring = (df['date'] >= '2024-03-21') & (df['date'] <= '2024-06-20')
    summer = (df['date'] >= '2024-06-21') & (df['date'] <= '2024-09-20')
    fall = (df['date'] >= '2024-09-21') & (df['date'] <= '2024-12-20')

    seasons = {
        'Winter': df[winter],
        'Spring': df[spring],
        'Summer': df[summer],
        'Fall': df[fall]
    }

    season_data = seasons.get(season, pd.DataFrame())
    if season_data.empty:
        assert np.isnan(expected_min_temp)
        assert np.isnan(expected_max_temp)
        assert np.isnan(expected_mean_temp)
    else:
        assert season_data['tavg'].min() == expected_min_temp
        assert season_data['tavg'].max() == expected_max_temp
        assert np.isclose(season_data['tavg'].mean(), expected_mean_temp, atol=0.1)

def test_season_stats_df(sample_df):
    df = sample_df
    df['date'] = pd.to_datetime(df['date'])

    # Adjusted date ranges to match the sample dataset
    winter = (df['date'] >= '2023-12-01') & (df['date'] <= '2023-12-10')
    spring = (df['date'] >= '2024-03-21') & (df['date'] <= '2024-06-20')
    summer = (df['date'] >= '2024-06-21') & (df['date'] <= '2024-09-20')
    fall = (df['date'] >= '2024-09-21') & (df['date'] <= '2024-12-20')

    seasons = {
        'Winter': df[winter],
        'Spring': df[spring],
        'Summer': df[summer],
        'Fall': df[fall]
    }

    season_stats = []
    for season, data in seasons.items():
        if data.empty:
            continue
        stats = {
            'Season': season,
            'Min Temp (°C)': data['tavg'].min(),
            'Max Temp (°C)': data['tavg'].max(),
            'Mean Temp (°C)': data['tavg'].mean(),
        }
        season_stats.append(stats)

    season_stats_df = pd.DataFrame(season_stats)
    assert 'Season' in season_stats_df.columns
    assert len(season_stats_df) > 0
