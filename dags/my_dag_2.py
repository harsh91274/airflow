from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from datetime import datetime
from random import randint 

# def _training_model():
#     return randint(1,10)

def _choose_best_model():
    accuracies=ti.xcom_pull(task_ids=['training_model_A', 'training_model_B', 'training_model_C'])
    best_accuracy=max(accuracies)

    if (best_accuracy >8):
        return "accurate"
    
    return 'inaccurate'

with DAG("my_dag2", start_date=datetime(2025, 3, 3), schedule="@daily", description="training ML models", tags=["data engineering team"], catchup=False) as dag2:
    
    @task
    def training_model(accuracy):
        return accuracy
    # training_model_A=PythonOperator(
    #     task_id="training_model_A",
    #     python_callable=_training_model, 
    # )

    # training_model_B=PythonOperator(
    #     task_id="training_model_B",
    #     python_callable=_training_model, 
    # )

    # training_model_C=PythonOperator(
    #     task_id="training_model_C",
    #     python_callable=_training_model, 
    # )

    choose_best_model=BranchPythonOperator(
        task_id="choose_best_model",
        python_callable=_choose_best_model
    )

    @task.branch
    def choose_best_model(accuracies):
        best_accuracy=max(accuracies)

        if (best_accuracy >8):
            return "accurate"
        
        return 'inaccurate'

    accurate=BashOperator(
        task_id="accurate",
        bash_command="echo 'accurate'"
    )

    inaccurate=BashOperator(
        task_id="inaccurate",
        bash_command="echo 'inaccurate'"
    )

    #[training_model_A, training_model_B, training_model_C] >> choose_best_model >> [accurate, inaccurate]

    choose_best_model(training_model.expand(accuracy=[3, 9, 2])) >> [accurate, inaccurate]