from airflow import DAG, Dataset
from airflow.decorators import task
from datetime import datetime
from include.datasets import MY_FILE

#my_file= Dataset("/tmp/my_file.txt")

with DAG(
    dag_id='consumer',
    schedule=[MY_FILE],
    start_date=datetime(2025, 3, 4),
    catchup=False,
):
    @task(outlets=[MY_FILE])
    def read_my_file():
        with open(MY_FILE.uri, "r") as f:
            print(f.read())
    
    read_my_file()
    
