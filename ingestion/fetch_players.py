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

TEAM_IDS = [
    1, 2, 3, 6, 7, 9, 10, 12, 13, 14,
    15, 16, 17, 20, 21, 22, 23, 24, 25, 26,
    27, 28, 29, 31, 767, 1118, 1504, 1530, 1569, 2382,
    2384, 5529
]

# ── Fetch Players ────────────────────────────────────────
def fetch_players(team_id):
    url = "https://v3.football.api-sports.io/players"
    params = {"team": team_id, "season": 2022}
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    if data['response']:
        return data['response']
    return []

# ── Save to PostgreSQL ───────────────────────────────────
def save_players(team_id, players):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw.players (
            id          SERIAL PRIMARY KEY,
            team_id     INTEGER,
            player_id   INTEGER,
            data        JSONB,
            fetched_at  TIMESTAMP DEFAULT NOW()
        );
    """)

    saved = 0
    for player in players:
        player_id = player['player']['id']
        cur.execute("""
            INSERT INTO raw.players (team_id, player_id, data)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, (team_id, player_id, json.dumps(player)))
        saved += 1

    conn.commit()
    cur.close()
    conn.close()
    return saved

# ── Main ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("Fetching World Cup 2022 players...")
    total = 0
    for team_id in TEAM_IDS:
        print(f"  Fetching players for team {team_id}...")
        players = fetch_players(team_id)
        if players:
            saved = save_players(team_id, players)
            total += saved
        time.sleep(0.5)

    print(f"Saved {total} players to PostgreSQL ✅")