SELECT 
    name,
    nationality,
    team,
    SUM(goals) as total_goals
from {{ref('stg_players')}}
GROUP BY name, nationality, team
HAVING SUM(goals) > 0
ORDER BY total_goals DESC
