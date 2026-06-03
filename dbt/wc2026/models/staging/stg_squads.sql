SELECT
    team_id,
    team_name,
    player_id,
    player_name,
    CAST(age as INTEGER) as age,
    CAST(number as INTEGER) as number,
    position
from analytics.squads
WHERE player_name IS NOT NULL