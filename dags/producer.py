from airflow import DAG, Dataset
from airflow.decorators import task
from include.datasets import MY_FILE
from datetime import datetime

#my_file= Dataset("/tmp/my_file.txt")

with DAG(
    dag_id='producer',
    schedule='@daily',
    start_date=datetime(2025, 3, 4),
    catchup=False,
):
    @task(outlets=[MY_FILE])
    def update_my_file():
        with open(MY_FILE.uri, "a+") as f:
            f.write("producer update")
    
    update_my_file()

