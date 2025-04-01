# api.py
import os
import fastapi
from fastapi import FastAPI
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve database connection details
DB_NAME = os.getenv("DB_NAME", "your_db_name")
DB_USER = os.getenv("DB_USER", "your_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Build the connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Initialize FastAPI
app = FastAPI()

@app.get("/passing-stats")
def get_passing_stats():
    """
    Retrieve all passing stats from the database.
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM man_city_passing_stats"))
        data = [dict(row._mapping) for row in result]
    return data
