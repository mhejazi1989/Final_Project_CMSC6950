Here’s the corrected version of the note with improved formatting and consistency:
________________________________________
Final Project CMSC6950 - Tehran Weather Analysis
This repository, hosted at mhejazi1989/Final_Project_CMSC6950, contains the code, scripts, and resources for analyzing Tehran's weather data from October 2023 to September 2024. The project investigates temperature and precipitation trends, extreme weather events, and correlations among key meteorological variables.
Project Objectives
1.	Analyze daily temperature and precipitation trends.
2.	Detect and visualize extreme values using statistical methods.
3.	Explore correlations between key variables.
4.	Categorize temperatures by thresholds and analyze seasonal variations.
Repository Structure
The repository is organized as follows:
•	Figures and Scripts: Each figure corresponds to a specific analysis, detailed below.
•	Test Scripts: Unit test scripts for each main script ensure accuracy and reproducibility.
Code Overview
Figure 1: Temperature Trends Over Time
•	Script: temperature_analysis1.py
•	Test Script: test_temperature_analysis1.py
Figure 2: Threshold-Based Temperature Categorization
•	Script: temp_threshold_analysis_2.py
•	Test Script: test_temp_threshold_analysis2.py
Figure 3: Outlier Detection in Seasonal Temperature Data
•	Script: detect_outliers_3.py
•	Test Script: test_detect_outliers3.py
Figure 4: Seasonal Temperature Heatmap
•	Script: heatmap_4.py
Figure 5: Statistical Distributions of Weather Data
•	Script: analyze_distributions_5.py
•	Test Script: test_analyze_distributions5.py
Figure 6: Temperature and Precipitation Trends
•	Script: temp_precip_analysis_6.py
•	Test Script: test_temp_precip_analysis6.py
Figure 7: Seasonal Statistics for Temperature, Precipitation, and Wind Speed
•	Script: seasonal_statistics_7.py
•	Test Script: test_seasonal_statistics7.py
Figure 8: Correlation Heatmap and Pairplot
•	Script: correlation_heatmap_pairplot_8.py
________________________________________
Getting Started
Prerequisites
Ensure you have the following installed:
•	Python 3.8+
•	Required libraries: pandas, numpy, matplotlib, seaborn, scipy, pytest
Installation
1.	Clone the repository: 
2.	git clone https://github.com/mhejazi1989/Final_Project_CMSC6950.git
3.	Navigate to the directory: 
4.	cd Final_Project_CMSC6950
5.	Install dependencies: 
6.	pip install -r requirements.txt
Usage
1.	Run the main scripts to generate figures. For example, to create Figure 1: 
2.	python temperature_analysis1.py
3.	To test a script, use the corresponding test file. For example: 
4.	pytest test_temperature_analysis1.py
________________________________________
Outputs
Figures
•	Figure 1: Temperature trends with extreme values highlighted.
•	Figure 2: Categorization of days based on ±1.5 standard deviation thresholds.
•	Figure 3: Boxplots showing seasonal temperature distributions before and after outlier removal.
•	Figure 4: Seasonal heatmap illustrating temperature variations.
•	Figure 5: Histograms and KDE plots showing distributions of key variables.
•	Figure 6: Combined plot of temperature and precipitation trends, with correlations.
•	Figure 7: Seasonal statistics visualized as grouped bar charts with a summary table.
•	Figure 8: Correlation heatmap and pairplot of weather variables.
________________________________________
Contributing
Contributions are welcome! Please fork the repository and create a pull request with detailed information about your changes.

