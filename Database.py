# PostgreSQL connection helpers.
import os
from pathlib import Path

import psycopg2

# Declare root
ROOT = Path(__file__).resolve().parent

# Database configuration dictionary
DATA_BASE_CONFIGURATIONS = {
    # Declare host - localhost
    "host": os.getenv("DB_HOST", "localhost"),

    # Declare user - root
    "port": os.getenv("DB_PORT", "5432"),

    # Declare name of database
    "dbname": os.getenv("DB_NAME", "Weather"),

    # Declare Postgres username
    "user": os.getenv("DB_USER", "kdrewes"),

    # Declare password - whatever you decide
    "password": os.getenv("DB_PASSWORD", ""), 

}

# Establish connection
def GetConnection():
    return psycopg2.connect(**DATA_BASE_CONFIGURATIONS)

# Execute schema.sql
def Run_Schema(schema_path: str | Path) -> None:

    # Declare path
    path = Path(schema_path)

    # Read schema.sql from disk and transfer text to PostgreSQL
    sql = path.read_text(encoding="utf-8")

    # Instantiate connection
    conn = GetConnection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
        print(f"Ran schema -> {path.relative_to(ROOT)}")
    finally:
        conn.close()

# Test to ensure application can connect to PostgreSQL
def TestConnection() -> None:
    try:

        # Instantiate connection
        conn = GetConnection()
        conn.close()

        # Print status of secure connection
        print("PostgreSQL connection OK.")

    except psycopg2.OperationalError as exc:

        # Print status of failed connection
        print("PostgreSQL connection failed.")
        print(f"  {exc}")

        # Provide steps used to connect to database
        print("\nNext steps:")
        print("  1. Install PostgreSQL")
        print("  2. Start server")
        print("  3. Create database: CREATE DATABASE weather_db;")
        print("  4. Update DB password in Database.py or a .env file")

# Execute main
if __name__ == "__main__":
    print(f"psycopg2 version: {psycopg2.__version__}")
    TestConnection()
