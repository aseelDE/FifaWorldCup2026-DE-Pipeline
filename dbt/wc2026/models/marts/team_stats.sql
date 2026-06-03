SELECT
    team_name,
    COUNT(player_id) AS total_players,
    COUNT(DISTINCT position) AS positions_count
FROM {{ ref('stg_squads') }}
GROUP BY team_name
ORDER BY team_name