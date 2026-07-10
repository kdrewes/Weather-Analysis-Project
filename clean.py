# Clean information

import json
from pathlib import Path
import pandas as pd

# Date ranges of Open Mateo's whether API archives
START_DATE = "2026-01-01"
END_DATE = "2026-07-01"

# List of cities and state stored in a list dictionary
CITIES = [
    {"name": "Berkeley", "state": "CA"},
    {"name": "Oakland", "state": "CA"},
    {"name": "San Francisco", "state": "CA"},
]

# File path of codebase
ROOT = Path(__file__).resolve().parent

# Path of raw data folder
RAW_DATA_DIRECTORY = ROOT / "Data" / "Raw"

# Path of processed data folder
PROCESSED_DATA_DIRECTORY = ROOT / "Data" / "Processed"

# Path of csv file
CSV_FILE = PROCESSED_DATA_DIRECTORY / "weather.csv"

# Tokenize city name from "San Francisco" to "san_francisco"
def TokenizeCity(city_name: str) -> str:
    return city_name.lower().replace(" ", "_")

# Produce city data frame
def CityDataFrame(city: dict) -> pd.DataFrame:
    
    # Declare variable that stores tokenized city name 
    tokenName = TokenizeCity(city["name"])

    # file path of json data for city of a particular date
    path = RAW_DATA_DIRECTORY / f"{tokenName}_{START_DATE}_{END_DATE}.json"

   # Read from the following file - RAW_DATA_DIRECTORY / f"{tokenName}_{START_DATE}_{END_DATE}.json
    with path.open(encoding="utf-8") as f:
        payload = json.load(f)

    # payload is a dictionary. 
    # One of its values is another dictionary called "daily". 
    # Inside "daily", each value is a list.
    daily = payload["daily"]

    # Return data frame
    return pd.DataFrame({
        "city": city["name"],
        "state": city["state"],
        "date": pd.to_datetime(daily["time"]),
        "temp_max_c": daily["temperature_2m_max"],
        "temp_min_c": daily["temperature_2m_min"],
        "wind_speed_max_kmh": daily["wind_speed_10m_max"],
        "rain_mm": daily["rain_sum"],
    })

# Display data cleaned frame
def PrintDataFrame(df: pd.DataFrame, label: str) -> None:
    
    # Display banned 
    print(f"\n{'=' * 50}")

    print(f"PROFILE: {label}")

    print(f"{'=' * 50}")

    # Print # of records
    print(f"Rows: {len(df)}")

    # Print data range
    print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")

    # Print missing values in each column
    print("\nNull counts:")
    print(df.isna().sum())

    # Print existing data types
    print("\nData types:")

    print(df.dtypes)

    # Print data type rangers
    print("\nNumeric summary:")

    print(df.describe())

    # Count duplicated rows
    dupes = df.duplicated(subset=["city", "date"]).sum()

    print(f"\nDuplicates on (city, date): {dupes}")

    # Declare sum of how many max values are less than min values
    invalid_temps = (df["temp_max_c"] < df["temp_min_c"]).sum()

    # Declare sum of how the quantity of negative values of rain_mm
    negative_rain = (df["rain_mm"] < 0).sum()

    # Print sum of how many max values are less than min values
    print(f"Days where max < min temp: {invalid_temps}")

    # Declare sum of how the quantity of negative values of rain_mm
    print(f"Negative rain values: {negative_rain}")

# Clean data frame
def CleanDataFrame(df: pd.DataFrame) -> pd.DataFrame:
    
    # Copy data frame
    cleaned = df.copy()

    # Drop duplicates from city and dates
    cleaned = cleaned.drop_duplicates(subset=["city", "date"])

    # If rain_nm is a negative number, assign it the value of zero 
    cleaned.loc[cleaned["rain_mm"] < 0, "rain_mm"] = 0

    # Preserve rows where maximum temp is greater than minimum temp.
    # Remove rows where maximum temp is less than minimum temp.
    cleaned = cleaned[cleaned["temp_max_c"] >= cleaned["temp_min_c"]]

    # Drop rows with missing temperature values if temp_max_c or temp_min_c is missing
    cleaned = cleaned.dropna(subset=["temp_max_c", "temp_min_c"])

    # Fill missing rain_mm with 0 for any null values
    cleaned["rain_mm"] = cleaned["rain_mm"].fillna(0)

    # Fill missing wind_speed_max_kmh with 0 for any null values
    cleaned["wind_speed_max_kmh"] = cleaned["wind_speed_max_kmh"].fillna(0)

    # Sort values by city and dates then reset values of cleaned data frame
    cleaned = cleaned.sort_values(["city", "date"]).reset_index(drop=True)

    # Return cleaned values
    return cleaned


def main() -> None:
    frames = [CityDataFrame(city) for city in CITIES]
    combined = pd.concat(frames, ignore_index=True)

    # Profile each city + combined
    for city in CITIES:
        city_df = combined[combined["city"] == city["name"]]
        PrintDataFrame(city_df, city["name"])
    PrintDataFrame(combined, "ALL CITIES")

    # Clean
    cleaned = CleanDataFrame(combined)
    print(f"\nRows before clean: {len(combined)}")
    print(f"Rows after clean:  {len(cleaned)}")

    # Save
    PROCESSED_DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(CSV_FILE, index=False)
    print(f"\nSaved -> {CSV_FILE.relative_to(ROOT)}")
    print("Complete.")


if __name__ == "__main__":
    main()