from airflow.decorators import dag, task
from airflow.utils import timezone
from datetime import timedelta

@dag(start_date=timezone.utcnow() - timedelta(days=1), 
     schedule="*/30 * * * *", 
     catchup=False)
def example_dag():

    @task
    def task1():
        print("Это код первой задачи")
        return "Результат task1"

    @task
    def task2(value):
        print(f"Получено из task1: {value}")
        print("Это код второй задачи")

    t1 = task1()
    t2 = task2(t1)  # передаем результат task1 в task2

example_dag()