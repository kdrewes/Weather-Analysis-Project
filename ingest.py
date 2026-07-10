# Retrieve daily weather data from Open-Meteo API and save raw JSON.

import json

from pathlib import Path

import requests

# URL used to import data from Open Mateo's API
API_BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

# Date ranges of Open Mateo's whether API archives
START_DATE = "2026-01-01"
END_DATE = "2026-07-01"

# List of cities which include: Berkeley, Oakland, San Francisco
CITIES = [
    {
        "name": "Berkeley",
        "state": "CA",
        "latitude": 37.88456729555717,
        "longitude": -122.27248805314625,
        "timezone": "America/Los_Angeles",
    },

    {
        "name": "Oakland",
        "state": "CA",
        "latitude": 37.80292052990092,
        "longitude": -122.22711266224863,
        "timezone": "America/Los_Angeles",
    },
    
    {
        "name": "San Francisco",
        "state": "CA",
        "latitude": 37.763642492775034,
        "longitude": -122.44206704116907,
        "timezone": "America/Los_Angeles",
    },
]

VARIABLES = [
    "temperature_2m_max", # Highest temperature
    "temperature_2m_min", # Lowest temperature
    "wind_speed_10m_max", # Wind speed
    "rain_sum",           # Sum of daily rain
]

# File paths
ROOT = Path(__file__).resolve().parent        # File path of codebase
RAW_DATA_DIRECTORY = ROOT / "Data" / "Raw"    # Path of data folder
SAMPLES_DIRECTORY = ROOT / "Samples"          # Path of sample folder


# Retreive data from Open Mateo and return result as dictionary
def RetrieveWeather(city: dict) -> dict:
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "start_date": START_DATE,
        "end_date": END_DATE,
        "daily": ",".join(VARIABLES),
        "timezone": city["timezone"],
    }

    # Submit GET request to Open Mateo
    response = requests.get(API_BASE_URL, params=params, timeout=30)
    
    # Raise error if API return status code of 4/5
    response.raise_for_status()

    # Return json response
    return response.json()

# Write dictionary into file.  Convert dictionary into JSON
def SaveJson(data: dict, filepath: Path) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with filepath.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# Tokenize city name from "San Francisco" to "san_francisco"
def TokenizeCity(city_name: str) -> str:
    return city_name.lower().replace(" ", "_")

def main() -> None:

    # Display date of weather data
    print(f"Retrieving weather: {START_DATE} to {END_DATE}")

    # Traverse through name of city in CITIES dictionary 
    print(f"Cities: {', '.join(c['name'] for c in CITIES)}\n")

    # Traverse through each city
    for city in CITIES:

        # Retrieve name of city
        tokenName = TokenizeCity(city["name"])

        # file path of json data for city of a particular date
        path = RAW_DATA_DIRECTORY / f"{tokenName}_{START_DATE}_{END_DATE}.json"

        # Dsiplay city and state data
        print(f"{city['name']}, {city['state']}...")

        # Weather data dictionary which will be transformed into payload
        payload = RetrieveWeather(city)

        # Create folder of weather data for particular city and date
        SaveJson(payload, path)

        # Display file was saved to data path
        print(f"\nSaved -> {path.relative_to(ROOT)}")

        # Declare variable for sample path directory
        samplePath = SAMPLES_DIRECTORY / f"{tokenName}_sample.json"

        # Copy from raw data directory to Samples folder
        SaveJson(json.loads(path.read_text(encoding="utf-8")), samplePath)

        # Display results
        print(f"\nSample response -> {samplePath.relative_to(ROOT)}")

    # Operation is complete
    print("\nComplete\n")

if __name__ == "__main__":
    main()
