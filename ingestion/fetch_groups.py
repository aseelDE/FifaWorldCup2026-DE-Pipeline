import requests
import psycopg2
import json
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

API_KEY = os.getenv("API_FOOTBALL_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

HEADERS = {"x-apisports-key": API_KEY}

def fetch_groups():
    url = "https://v3.football.api-sports.io/standings"
    params = {"league": 1, "season": 2022}
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    print(f"Groups fetched: {len(data['response'])}")
    return data['response']

def save_groups(groups):
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT,
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw.groups (
            id          SERIAL PRIMARY KEY,
            data        JSONB,
            fetched_at  TIMESTAMP DEFAULT NOW()
        );
    """)

    cur.execute("TRUNCATE TABLE raw.groups;")
    inserted = 0
    for group in groups:
        cur.execute("""
            INSERT INTO raw.groups (data) VALUES (%s);
        """, (json.dumps(group),))

    conn.commit()
    cur.close()
    conn.close()
    print(f"Saved {len(groups)} groups to PostgreSQL ✅")

if __name__ == "__main__":
    print("Fetching World Cup 2022 groups...")
    groups = fetch_groups()
    if groups:
        save_groups(groups)
    else:
        print("No groups found.")