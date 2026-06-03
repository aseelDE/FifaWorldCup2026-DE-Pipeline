from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, get_json_object
import os

# DB config
DB_HOST = os.environ.get("DB_HOST", "de_postgres")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "wc2026_db")
DB_USER = os.environ.get("DB_USER", "de_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "de_password")
JDBC_URL = f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}"
JDBC_DRIVER = "/opt/spark/jars/extra/postgresql-42.7.11.jar"

# Create Spark Session
spark = SparkSession.builder \
    .appName("WC2026_process_raw") \
    .config("spark.jars", JDBC_DRIVER) \
    .getOrCreate()

# JDBC properties
jdbc_properties = {
    "user": DB_USER,
    "password": DB_PASSWORD,
    "driver": "org.postgresql.Driver"
}

# Read table from PostgreSQL
def read_table(table_name):
    return spark.read \
        .jdbc(url=JDBC_URL,
              table=table_name,
              properties=jdbc_properties)

# Process fixtures
def process_fixtures():
    df = read_table("raw.fixtures")
    return df.select(
        get_json_object(col("data"), "$.fixture.id").alias("fixture_id"),
        get_json_object(col("data"), "$.fixture.date").alias("date"),
        get_json_object(col("data"), "$.teams.home.name").alias("home_team"),
        get_json_object(col("data"), "$.teams.away.name").alias("away_team"),
        get_json_object(col("data"), "$.goals.home").alias("home_goals"),
        get_json_object(col("data"), "$.goals.away").alias("away_goals"),
        get_json_object(col("data"), "$.fixture.status.short").alias("status")
    )

# Process players
def process_players():
    df = read_table("raw.players")
    return df.select(
        get_json_object(col("data"), "$.player.id").alias("player_id"),
        get_json_object(col("data"), "$.player.name").alias("name"),
        get_json_object(col("data"), "$.player.nationality").alias("nationality"),
        get_json_object(col("data"), "$.player.age").alias("age"),
        get_json_object(col("data"), "$.statistics[0].team.name").alias("team"),
        get_json_object(col("data"), "$.statistics[0].goals.total").alias("goals"),
        get_json_object(col("data"), "$.statistics[0].games.rating").alias("rating")
    )

# Process groups
def process_groups():
    df = read_table("raw.groups")
    from pyspark.sql.functions import from_json, schema_of_json
    from pyspark.sql.types import ArrayType, StructType, StructField, StringType, IntegerType

    standings_schema = ArrayType(ArrayType(StructType([
        StructField("rank", IntegerType()),
        StructField("group", StringType()),
        StructField("points", IntegerType()),
        StructField("goalsDiff", IntegerType()),
        StructField("team", StructType([
            StructField("id", IntegerType()),
            StructField("name", StringType())
        ])),
        StructField("all", StructType([
            StructField("played", IntegerType()),
            StructField("win", IntegerType()),
            StructField("draw", IntegerType()),
            StructField("lose", IntegerType())
        ]))
    ])))

    df = df.withColumn("standings", from_json(
        get_json_object(col("data"), "$.league.standings"),
        standings_schema
    ))
    df = df.select(explode(col("standings")).alias("group_array"))
    df = df.select(explode(col("group_array")).alias("team"))
    return df.select(
        col("team.rank").alias("rank"),
        col("team.team.name").alias("team_name"),
        col("team.group").alias("group_name"),
        col("team.points").alias("points"),
        col("team.goalsDiff").alias("goals_diff"),
        col("team.all.win").alias("wins"),
        col("team.all.draw").alias("draws"),
        col("team.all.lose").alias("losses"),
        col("team.all.played").alias("played")
    )

# Process squads
def process_squads():
    df = read_table("raw.squads")
    from pyspark.sql.functions import from_json
    from pyspark.sql.types import ArrayType, StructType, StructField, StringType, IntegerType

    players_schema = ArrayType(StructType([
        StructField("id", IntegerType()),
        StructField("name", StringType()),
        StructField("age", IntegerType()),
        StructField("number", IntegerType()),
        StructField("position", StringType())
    ]))

    df = df.withColumn("team_id", get_json_object(col("data"), "$.team.id"))
    df = df.withColumn("team_name", get_json_object(col("data"), "$.team.name"))
    df = df.withColumn("players", from_json(
        get_json_object(col("data"), "$.players"),
        players_schema
    ))
    df = df.select(
        col("team_id"),
        col("team_name"),
        explode(col("players")).alias("player")
    )
    return df.select(
        col("team_id"),
        col("team_name"),
        col("player.id").alias("player_id"),
        col("player.name").alias("player_name"),
        col("player.age").alias("age"),
        col("player.number").alias("number"),
        col("player.position").alias("position")
    )

# Write table to PostgreSQL
def write_table(df, table_name):
    df.write \
        .jdbc(url=JDBC_URL,
              table=table_name,
              mode="overwrite",
              properties=jdbc_properties)

# Main
if __name__ == "__main__":
    print("Processing fixtures...")
    write_table(process_fixtures(), "analytics.fixtures")
    print("Fixtures done! ✅")

    print("Processing groups...")
    write_table(process_groups(), "analytics.standings")
    print("Groups done! ✅")

    print("Processing squads...")
    write_table(process_squads(), "analytics.squads")
    print("Squads done! ✅")

    print("Processing players...")
    write_table(process_players(), "analytics.players")
    print("Players done! ✅")

    spark.stop()
    print("All done! 🎉")