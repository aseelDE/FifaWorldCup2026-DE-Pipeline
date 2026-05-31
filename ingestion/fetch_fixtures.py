import requests
import psycopg2
import json
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

# ── Config ──────────────────────────────────────────────
API_KEY = os.getenv("API_FOOTBALL_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

HEADERS = {
    "x-apisports-key": API_KEY
}

# ── Fetch Fixtures ───────────────────────────────────────
def fetch_fixtures():
    url = "https://v3.football.api-sports.io/fixtures"
    params = {
        "league": 1,
        "season": 2022
    }
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    print("Full API response:", json.dumps(data, indent=2))
    print(f"Total fixtures fetched: {len(data['response'])}")
    return data['response']

# ── Save to PostgreSQL ───────────────────────────────────
def save_fixtures(fixtures):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw.fixtures (
            fixture_id   INTEGER PRIMARY KEY,
            data         JSONB,
            fetched_at   TIMESTAMP DEFAULT NOW()
        );
    """)

    inserted = 0
    for fixture in fixtures:
        fixture_id = fixture['fixture']['id']
        cur.execute("""
            INSERT INTO raw.fixtures (fixture_id, data)
            VALUES (%s, %s)
            ON CONFLICT (fixture_id) DO UPDATE SET
                data = EXCLUDED.data,
                fetched_at = NOW();
        """, (fixture_id, json.dumps(fixture)))
        inserted += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"Saved {inserted} fixtures to PostgreSQL ✅")

# ── Main ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("Fetching World Cup 2026 fixtures...")
    fixtures = fetch_fixtures()
    if fixtures:
        save_fixtures(fixtures)
    else:
        print("No fixtures found. Check your API key or league ID.")