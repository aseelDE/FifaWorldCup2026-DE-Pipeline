SELECT
    fixture_id,
    match_date,
    home_team,
    away_team,
    home_goals,
    away_goals,
    CASE
        WHEN home_goals > away_goals THEN 'Home Win'
        WHEN away_goals > home_goals THEN 'Away Win'
        ELSE 'Draw'
    END AS result
FROM {{ ref('stg_fixtures') }}
WHERE status = 'FT'
AND fixture_id >= '855795'