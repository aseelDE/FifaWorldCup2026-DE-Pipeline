SELECT 
     player_id,
     name,
     nationality,
     CAST(age AS INTEGER) as age,
     team,
     CAST(goals AS INTEGER) as goals,
     CAST(rating AS NUMERIC (4,2)) as rating
from analytics.players
WHERE name IS NOT NULL