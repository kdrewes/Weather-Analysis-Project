# Project 1 Summary — Weather Analytics Platform

## Cities and Date Range

This project analyzes daily weather data for three Bay Area cities:

- Berkeley, CA
- Oakland, CA
- San Francisco, CA

Summary:

Data was collected from the Open-Meteo Historical Weather API for the date range
- 2026-01-01 to 2026-07-01 (182 days) for Berkeley, Oakland and San Francisco

Data extracted from the Open-Meteo Historical Weather API includes daily weather metrics for each city: 

• Maximum temperature (temp_max_c)
• Minimum temperature (temp_min_c)
• Maximum wind speed (wind_speed_max_kmh) 
• Total daily rainfall (rain_mm). 

## Cleaning Process

Data wrangling was performed through Pandas.  The following operations were implemented:

• Elimination of null values
• Filtering duplicates
• Detection of invalid temperatures
• Filter row where temp_max_c < temp_min_c
• Filled missing `rain_mm` and `wind_speed_max_kmh` with 0

## Analysis

Five SQL queries in `queries.sql` perform operations such as:

• Hottest day of the year per city
• Average rainfall, 
• Monthly precipitation, 
• Peak wind per week of each city
• Frequency of extreme heat days over 88 degree fahrenheit.

