from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime



#define_DAGs

with DAG (
    dag_id = "wc_pre_tournament_dag",
    start_date = datetime(2026,6,1),
    schedule_interval = "@daily",
    catchup = False
) as dag:

    fetch_fixtures = BashOperator(
        task_id = "fetch_fixtures",
        bash_command="python /opt/airflow/ingestion/fetch_fixtures.py"
    )

    fetch_groups = BashOperator(
        task_id = "fetch_groups",
        bash_command="python /opt/airflow/ingestion/fetch_groups.py"
    )

    fetch_squads = BashOperator(
        task_id = "fetch_squads",
        bash_command="python /opt/airflow/ingestion/fetch_squads.py"
    )

    fetch_players = BashOperator(
        task_id = "fetch_players",
        bash_command="python /opt/airflow/ingestion/fetch_players.py"
    )

    fetch_fixtures >> fetch_groups >> fetch_squads >> fetch_players
    