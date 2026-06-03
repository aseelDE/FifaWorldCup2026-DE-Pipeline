SELECT 
    fixture_id,
    date as match_date,
    home_team,
    away_team,
    CAST(home_goals AS INTEGER) AS home_goals,
    CAST(away_goals AS INTEGER) AS away_goals,
    status
from analytics.fixtures