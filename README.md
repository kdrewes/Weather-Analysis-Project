# Project 1 Summary — Weather Analytics Platform

## Cities and Date Range

This project analyzes daily weather data for three Bay Area cities:

• Berkeley, CA<br>
• Oakland, CA<br>
• San Francisco, CA<br>

Summary:

Data was collected from the Open-Meteo Historical Weather API for the date range<br>
- 2026-01-01 to 2026-07-01 (182 days) for Berkeley, Oakland and San Francisco

Data extracted from the Open-Meteo Historical Weather API includes daily weather metrics for each city: 

• Maximum temperature (temp_max_c)<br>
• Minimum temperature (temp_min_c)<br>
• Maximum wind speed (wind_speed_max_kmh) <br>
• Total daily rainfall (rain_mm). <br>

## Cleaning Process

Data wrangling was performed through Pandas.  The following operations were implemented:

• Elimination of null values<br>
• Filtering duplicates<br>
• Detection of invalid temperatures<br>
• Filter row where temp_max_c < temp_min_c<br>
• Filled missing `rain_mm` and `wind_speed_max_kmh` with 0<br>

## Analysis

Five SQL queries in `queries.sql` perform operations such as:

• Hottest day of the year per city<br>
• Average rainfall, <br>
• Monthly precipitation, <br>
• Peak wind per week of each city<br>
• Frequency of extreme heat days over 88 degree fahrenheit.<br>

