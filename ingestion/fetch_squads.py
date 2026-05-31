import requests
import psycopg2
import json
import os
import time
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

HEADERS = {"x-apisports-key": API_KEY}

# World Cup 2022 team IDs
TEAM_IDS = [
    1, 2, 3, 6, 7, 9, 10, 12, 13, 14,
    15, 16, 17, 20, 21, 22, 23, 24, 25, 26,
    27, 28, 29, 31, 767, 1118, 1504, 1530, 1569, 2382,
    2384, 5529
]

# ── Fetch Squad ──────────────────────────────────────────
def fetch_squad(team_id):
    url = "https://v3.football.api-sports.io/players/squads"
    params = {"team": team_id}
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    if data['response']:
        return data['response'][0]
    return None

# ── Save to PostgreSQL ───────────────────────────────────
def save_squads(squads):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw.squads (
            team_id     INTEGER PRIMARY KEY,
            data        JSONB,
            fetched_at  TIMESTAMP DEFAULT NOW()
        );
    """)

    saved = 0
    for team_id, squad in squads:
        cur.execute("""
            INSERT INTO raw.squads (team_id, data)
            VALUES (%s, %s)
            ON CONFLICT (team_id) DO UPDATE SET
                data = EXCLUDED.data,
                fetched_at = NOW();
        """, (team_id, json.dumps(squad)))
        saved += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"Saved {saved} squads to PostgreSQL ✅")

# ── Main ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("Fetching World Cup 2022 squads...")
    results = []
    for team_id in TEAM_IDS:
        print(f"  Fetching team {team_id}...")
        squad = fetch_squad(team_id)
        if squad:
            results.append((team_id, squad))
        time.sleep(0.5)  # small delay to avoid hitting rate limits

    if results:
        save_squads(results)
    else:
        print("No squads found.")