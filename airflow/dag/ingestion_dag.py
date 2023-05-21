from datetime import timedelta, datetime

from airflow.decorators import dag, task_group

from airflow.dag.utils.utils import economic_variables

from airflow.dag.tasks.extract_from_api import extract_data_task

from airflow.dag.tasks.copy_to_redshift import copy_to_redshift


@dag(
dag_id="economic_data_visualization_dag",
    start_date=datetime(2020, 1, 1),
    catchup=True,
    schedule_interval="@daily",
    max_active_tasks=12,
    default_args={
        "retries": 3,
        "retry_delay": timedelta(minutes=5)})
def economic_data_visualization_dag():
    for variable in economic_variables:
        @task_group(group_id=f"process_{variable}")
        def process_variable():
            extract_data_task(variable)>>copy_to_redshift()>>load_data_into_powerbi_task()
