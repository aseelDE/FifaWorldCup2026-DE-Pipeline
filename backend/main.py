from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env
load_dotenv(Path(__file__).parent.parent / ".env")

# DB config
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "wc2026_db"),
    "user": os.getenv("DB_USER", "de_user"),
    "password": os.getenv("DB_PASSWORD", "de_password")
}

# FastAPI app
app = FastAPI(
    title="FIFA World Cup 2026 API",
    description="Data Engineering Pipeline API",
    version="1.0.0"
)

# CORS — allows Next.js frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# DB connection helper
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Query helper — runs SQL and returns list of dicts
def query(sql):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(row) for row in results]

# ── Endpoints ──────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "FIFA World Cup 2026 API is running!"}

@app.get("/matches")
def get_matches():
    return query("SELECT * FROM analytics.match_results ORDER BY match_date")

@app.get("/standings")
def get_standings():
    return query("SELECT * FROM analytics.group_standings ORDER BY group_name, rank")

@app.get("/top-scorers")
def get_top_scorers():
    return query("SELECT * FROM analytics.top_scorers ORDER BY total_goals DESC")

@app.get("/team-stats")
def get_team_stats():
    return query("SELECT * FROM analytics.team_stats ORDER BY team_name")

@app.get("/knockout")
def get_knockout():
    return query("SELECT * FROM analytics.knockout_results ORDER BY match_date")