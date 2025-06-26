from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    'simple_dag',
    start_date=datetime(2023, 1, 1),
    catchup=False
) as dag:
    task1 = BashOperator(
        task_id='task_1',
        bash_command='echo "Hello, World!"'
    )
    task2 = BashOperator(
        task_id='task_2',
        bash_command='echo "This is task 2"'
    )
    task1 >> task2