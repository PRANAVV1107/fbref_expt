import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from a .env file (if available)
load_dotenv()  # Looks for a .env file in the current directory

# Retrieve database connection details from environment variables
DB_NAME = os.getenv("DB_NAME", "your_db_name")
DB_USER = os.getenv("DB_USER", "your_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Create the SQLAlchemy engine for PostgreSQL
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Define the seasons you want to collect data for
years = ['2022-2023', '2023-2024', '2024-2025']
data_frames = []

# Loop through each season and collect data from FBref
for year in years:
    url = f"https://fbref.com/en/squads/b8fd03ef/{year}/matchlogs/all_comps/passing/Manchester-City-Match-Logs-All-Competitions"
    try:
        # Read tables from the URL (header row is assumed to be the second row, hence header=[1])
        tables = pd.read_html(url, header=[1])
        # Assume the first table contains the passing stats
        df = tables[0]
        data_frames.append(df)
        print(f"Data for {year} collected successfully.")
    except Exception as e:
        print(f"Failed to retrieve data for {year}: {e}")

# If any data was collected, combine them into one DataFrame and push to PostgreSQL
if data_frames:
    combined_df = pd.concat(data_frames, ignore_index=True)
    try:
        # Insert data into a table named "man_city_passing_stats" (it will be created automatically)
        combined_df.to_sql("man_city_passing_stats", engine, if_exists="append", index=False)
        print("Data inserted into the database successfully!")
    except Exception as e:
        print(f"Error inserting data into the database: {e}")
else:
    print("No data was collected.")
