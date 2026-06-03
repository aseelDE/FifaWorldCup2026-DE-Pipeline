SELECT
    group_name,
    rank,
    team_name,
    played,
    wins,
    draws,
    losses,
    points,
    goals_difference
FROM {{ ref('stg_standings') }}
ORDER BY group_name, rank