# CLAUDE.md — FIFA World Cup 2026 DE Pipeline
> Paste this file at the start of every new chat so Claude has full project context.

---

## 👤 About Me
- **Name:** Aseel Alzahrani
- **GitHub:** [aseelDE](https://github.com/aseelDE)
- **Goal:** Data Engineering portfolio project
- **PC:** Windows 11, Username: `Assel`

---

## 📁 Project Info
- **Project Name:** FIFA World Cup 2026 Data Engineering Pipeline
- **Portfolio Project #:** 4
- **Repo:** https://github.com/aseelDE/FifaWorldCup2026-DE-Pipeline
- **Local Path:** `C:\Users\Assel\FifaWorldCup2026-DE-Pipeline`
- **Description:** Real-time FIFA World Cup 2026 analytics pipeline built from scratch. Currently using 2022 World Cup data (free API plan) for development and testing. Will switch to 2026 live data before June 11, 2026 when upgrading to Pro API plan.

---

## 🛠️ Tech Stack

| Layer | Tool | Where It Runs |
|---|---|---|
| Ingestion | Python | Windows PC |
| Orchestration | Apache Airflow | Docker |
| Storage | PostgreSQL | Docker |
| Processing | Apache Spark | Docker |
| Transformation | dbt | Windows PC |
| Backend API | FastAPI | To be deployed (Railway/Render) |
| Frontend | Next.js + Tailwind | To be deployed (Vercel) |
| Version Control | GitHub | Public repo |

---

## 🐳 Docker Infrastructure
- **Infrastructure folder:** `C:\Users\Assel\de-infrastructure\`
- **Start command:** `docker-compose -f C:\Users\Assel\de-infrastructure\docker-compose.yml up -d`
- **Stop command:** `docker-compose -f C:\Users\Assel\de-infrastructure\docker-compose.yml down`
- **PostgreSQL container name:** `de_postgres`
- **DB credentials:**
  - Host: `localhost`
  - Port: `5432`
  - Database: `wc2026_db`
  - User: `de_user`
  - Password: `de_password`
  - Schemas: `raw` (raw JSON), `analytics` (clean tables)

---

## 📡 Data Source
- **API:** API-Football (api-football.com)
- **Current Plan:** Free (100 req/day, seasons 2022–2024 only)
- **Upgrade Plan:** Pro ($19/month) before June 11, 2026
- **World Cup League ID:** `1`
- **Current Season in use:** `2022` (Qatar World Cup)
- **Target Season:** `2026` (USA/Canada/Mexico)
- **Header key:** `x-apisports-key`

---

## 📂 Folder Structure
```
FifaWorldCup2026-DE-Pipeline/
├── ingestion/
│   ├── fetch_fixtures.py      ✅ Done
│   ├── fetch_groups.py        ✅ Done
│   ├── fetch_squads.py        ✅ Done
│   └── fetch_players.py       ✅ Done
├── airflow/
│   └── dags/
│       ├── wc_pre_tournament_dag.py   🔲 Phase 3 - Next
│       └── wc_live_dag.py             🔲 Phase 3 - Next
├── spark/
│   └── process_raw.py         🔲 Phase 4
├── dbt/
│   ├── models/
│   │   ├── staging/           🔲 Phase 5
│   │   └── marts/             🔲 Phase 5
│   └── tests/                 🔲 Phase 5
├── dashboard/
│   └── screenshots/
├── .env                       ✅ Done (never commit this)
├── .gitignore                 ✅ Done
└── README.md                  🔲 To be written
```

---

## 🗄️ PostgreSQL Tables (raw schema)

| Table | Rows | Description |
|---|---|---|
| raw.fixtures | 64 | All 2022 World Cup matches (full JSON) |
| raw.groups | 1 | All group standings (nested JSON) |
| raw.squads | 16 | National team squads (16/32 teams, free plan limit) |
| raw.players | 400 | Player profiles and stats |

---

## ✅ Completed Phases

### Phase 1 — Environment Setup ✅
- PostgreSQL running in Docker
- Apache Airflow running in Docker
- Apache Spark running in Docker
- GitHub repo created and connected
- Folder structure created
- `.env` and `.gitignore` configured
- `wc2026_db` database created with `raw` and `analytics` schemas

### Phase 2 — Data Ingestion ✅
- `fetch_fixtures.py` — fetches all 64 World Cup matches → `raw.fixtures`
- `fetch_groups.py` — fetches group standings → `raw.groups`
- `fetch_squads.py` — fetches team squads → `raw.squads`
- `fetch_players.py` — fetches player stats → `raw.players`
- All scripts use: `requests`, `psycopg2`, `python-dotenv`, `pathlib`
- Pattern: fetch from API → store raw JSON in PostgreSQL JSONB column

---

## 🔲 Remaining Phases

### Phase 3 — Airflow DAGs (NEXT)
- `wc_pre_tournament_dag.py` → runs daily, calls all 4 ingestion scripts
- `wc_live_dag.py` → runs every 5 min during matches, calls fixtures + groups
- Aseel wants to **learn and write DAGs herself** with guidance
- DAGs go in: `airflow/dags/`
- Airflow connects to scripts via `PythonOperator` or `BashOperator`

### Phase 4 — Spark Processing
- Read raw JSON from PostgreSQL
- Flatten nested JSON fields
- Calculate group stage qualification probabilities
- Calculate player tournament ratings
- Write processed data to `analytics` schema

### Phase 5 — dbt Transformation
- Staging models → clean raw data
- Mart models → analytics-ready tables
- Key models: `group_standings`, `player_tournament_rating`, `team_strength_index`, `knockout_bracket`, `live_match_momentum`, `head_to_head_history`, `top_scorers`
- dbt tests for data quality

### Phase 6 — FastAPI Backend
- Reads from PostgreSQL analytics schema
- Exposes REST endpoints for the frontend
- Deploy on Railway or Render (~$5/month)

### Phase 7 — Next.js Frontend (Public Website)
- Modern World Cup dashboard
- Live group standings, match scores, player stats, knockout bracket
- Target audience: football fans + recruiters
- Deploy on Vercel (free)
- Aseel will need help with modern UI design

### Phase 8 — Go Live (June 11, 2026)
- Upgrade API to Pro plan
- Switch all scripts from `season: 2022` to `season: 2026`
- Activate Airflow DAGs for live data
- Deploy backend and frontend

---

## 💡 Important Notes for Claude
- Aseel is learning — **always explain code line by line when asked**
- Aseel wants to **write scripts herself** when possible — guide, don't just give answers
- All Python scripts follow the same pattern: imports → load_dotenv → config → fetch function → save function → main block
- `.env` file is at the **project root**, scripts are in subfolders — always use `Path(__file__).parent.parent / ".env"` to load it
- Free API plan: use `season: 2022`, `league: 1`
- World Cup 2022 team IDs: `[1, 2, 3, 6, 7, 9, 10, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 767, 1118, 1504, 1530, 1569, 2382, 2384, 5529]`
- Bijaykund8 appears as contributor due to cached Git credentials on new PC — will disappear within 24hrs, already fixed
