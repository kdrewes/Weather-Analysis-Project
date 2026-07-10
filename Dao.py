# Data Access Object File

from pathlib import Path

import pandas as pd

from Database import GetConnection

# Root directory of dao.py
ROOT = Path(__file__).resolve().parent

# Cleaned CSV file originally processed through clean.py
CSV_FILE = ROOT / "Data" / "Processed" / "weather.csv"

# Insert city attributes into City entity
def InsertCity(cursor, name: str, state: str) -> int:
   
   # Add city and state into City entity.  
   # If city name exists, update it to current value without replacing
    cursor.execute(
        """INSERT INTO cities (name, state) VALUES (%s, %s) 
        ON CONFLICT (name) DO UPDATE SET state = EXCLUDED.state RETURNING city_id""",
        (name, state),
    )
    # Return first column of row
    return cursor.fetchone()[0]

# Insert weather record into Postgres database
def InsertWeatherRecord(cursor, city_id: int, row) -> None:
    
    # If row has a date call it, otherwise leave it how it is
    record_date = row["date"].date() if hasattr(row["date"], "date") else row["date"]

    # Insert attributes into weather entity
    cursor.execute(
        """
        INSERT INTO weather
            (city_id, record_date, temp_max_c, temp_min_c, wind_speed_max_kmh, rain_mm)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (city_id, record_date) DO UPDATE SET
            temp_max_c = EXCLUDED.temp_max_c,
            temp_min_c = EXCLUDED.temp_min_c,
            wind_speed_max_kmh = EXCLUDED.wind_speed_max_kmh,
            rain_mm = EXCLUDED.rain_mm
        """,
        (
            city_id,
            record_date,
            row["temp_max_c"],
            row["temp_min_c"],
            row["wind_speed_max_kmh"],
            row["rain_mm"],
        ),
    )

# Load weather.csv document
def LoadWeatherCsv(csv_path: str | Path = CSV_FILE) -> None:

    # Declare path variable
    path = Path(csv_path)

    # Read cleaned CSV into a DataFrame
    df = pd.read_csv(path, parse_dates=["date"])

    # Call connection
    conn = GetConnection()

    
    try:
        with conn.cursor() as cur:
            # Group city into Postgres SQL
            for (city_name, state), group in df.groupby(["city", "state"]):
                city_id = InsertCity(cur, city_name, state)

                for _, row in group.iterrows():
                    InsertWeatherRecord(cur, city_id, row)

        conn.commit()
        print(f"Loaded {len(df)} rows from {path.relative_to(ROOT)}")

    finally:
        conn.close()

# Count # of records
def CountRecords() -> None:
   
    conn = GetConnection()
    try:
        # 
        with conn.cursor() as cursor:

            # Implement count query to count # of rows from cities table
            cursor.execute("SELECT COUNT(*) FROM cities")

            # Fetch first column of row
            city_count = cursor.fetchone()[0]

         # Implement count query to count # of rows from weather table
            cursor.execute("SELECT COUNT(*) FROM weather")
            weather_count = cursor.fetchone()[0]

        # Display results
        print(f"Cities: {city_count}")
        print(f"Weather rows: {weather_count}")
    finally:
        conn.close()


# Execute main function
if __name__ == "__main__":
  LoadWeatherCsv()
  CountRecords()