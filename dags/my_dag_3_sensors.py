from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from datetime import datetime
from random import randint 
from airflow.sensors.filesystem import FileSensor

# def _training_model():
#     return randint(1,10)

def _choose_best_model():
    accuracies=ti.xcom_pull(task_ids=['training_model_A', 'training_model_B', 'training_model_C'])
    best_accuracy=max(accuracies)

    if (best_accuracy >8):
        return "accurate"
    
    return 'inaccurate'

with DAG("my_dag3_sensor", start_date=datetime(2025, 3, 3), schedule="@daily", catchup=False) as dag:
    
    waiting_for_file=FileSensor(
        task_id='waiting_for_file',
        poke_interval=30,
        timeout=60*5,
        mode='reschedule',
        soft_fail=True
    )