from airflow import dag


from airflow.hooks.S3_hook import S3Hook
from airflow.operators.hive_operator import HiveOperator

from airflow.dag.configs.configs import BUCKET_NAME

load_data_to_powerbi_task = HiveOperator(
    task_id='load_data_to_hive_task',
    hql=f'LOAD DATA INPATH \'s3://{BUCKET_NAME}/raw_data/*.csv\' INTO TABLE powerbi_data_table',
    dag=dag,
)