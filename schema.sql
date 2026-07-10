-- Drop existing tables if they are currently present
DROP TABLE IF EXISTS Weather;
DROP TABLE IF EXISTS Cities;

-- Model of each city
CREATE TABLE Cities 
(
    city_id SERIAL,
    name VARCHAR(100) NOT NULL UNIQUE,
    state CHAR(2) NOT NULL,
    PRIMARY KEY (city_id)
);

-- Model of daily weather per city
CREATE TABLE Weather 
(
    record_id SERIAL,
    city_id INTEGER NOT NULL,
    record_date DATE NOT NULL,
    temp_max_c NUMERIC(5, 2) NOT NULL,
    temp_min_c NUMERIC(5, 2) NOT NULL,
    wind_speed_max_kmh NUMERIC(6, 2) NOT NULL,
    rain_mm NUMERIC(6, 2) NOT NULL,
    
    UNIQUE (city_id, record_date),
    PRIMARY KEY (record_id),
    FOREIGN KEY (city_id) REFERENCES Cities(city_id)
);