# Final_Project_CMSC6950
Final_Project_CMSC6950_Fall2024
Tehran Weather Data Analysis
Project Overview
This project aims to analyze daily weather data for Tehran, Iran. The dataset contains multiple meteorological variables recorded over a year, including temperatures, precipitation, wind data, and atmospheric pressure. The goal is to inspect the dataset for missing values, summarize key weather metrics, and identify extreme weather events through statistical outlier detection. This analysis can help detect unusual weather patterns and lays the foundation for potential predictive modeling in future studies.

Dataset Description
The dataset includes 366 entries, each representing a day's weather data for one year. Key variables are:

date: Date of the record
tavg: Average temperature (°C)
tmin: Minimum temperature (°C)
tmax: Maximum temperature (°C)
prcp: Precipitation (mm)
snow: Snowfall (cm)
wdir: Wind direction (degrees)
wspd: Wind speed (m/s)
wpgt: Wind gust (m/s)
pres: Atmospheric pressure (hPa)
tsun: Sunshine duration (hours)
Analysis Workflow
Data Inspection and Missing Values:

Checked for missing values and noted that some variables (snow, wpgt, tsun) had significant gaps, which were addressed as necessary.
Summary Statistics:

Calculated descriptive statistics (mean, standard deviation, percentiles) for temperature (tavg, tmin, tmax) and precipitation (prcp) to understand the distribution of key variables.
Outlier Detection:

Applied two methods to detect extreme values:
Z-Score: Flagged values with z-scores beyond ±2 standard deviations as potential outliers.
Interquartile Range (IQR): Identified values outside 1.5 times the IQR from the 25th and 75th percentiles as extreme.
Seasonal Analysis:

Divided the dataset into four seasons (Winter, Spring, Summer, Fall) to calculate seasonal statistics for temperature and precipitation.
Visualizations:

Developed various plots to summarize and visualize trends in temperature and precipitation:
Time Series Line Plots: To observe day-by-day variations.
Box Plots: To show temperature and precipitation distribution across seasons.
Seasonal Bar Graphs: Depicting mean seasonal temperatures and precipitation.
Heatmaps: Monthly temperature and precipitation averages.
Scatter Plot with Trend Line: To explore relationships between temperature and precipitation.
Extreme Weather Events Analysis:

Defined thresholds to flag extreme temperature (based on percentiles) and heavy rainfall events (precipitation > 50 mm).
Summarized the frequency of extreme events per month to identify potential seasonal patterns.
Conclusion
The analysis highlights seasonal weather patterns and identifies outliers that could represent extreme weather events or data inaccuracies. This study provides initial insights that could be extended into forecasting models, potentially improving predictions for extreme weather conditions in Tehran.

How to Run This Project
Environment Setup:

Install the necessary Python libraries: pandas, matplotlib, and scipy.
Data Loading:

Load the dataset from TehranWeather.xlsx.
Run Analysis:

Execute the code cells sequentially to inspect data, calculate statistics, and produce visualizations.
Results Visualization:

The final graphs and tables will provide an overview of Tehran’s weather patterns across the year.
This project serves as a foundation for weather analysis and may be extended with predictive modeling techniques in future work.
