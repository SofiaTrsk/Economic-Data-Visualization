from datetime import timedelta

from airflow.decorators import dag, task_group

import logging
from datetime import datetime

import pandas as pd
import requests
from airflow.decorators import task

from airflow.configs import BASE_DIR, API_KEY, ACCESS_KEY, SECRET_KEY
from airflow.models import Variable

from airflow.utils.utils import clean_file, save_to_s3
# from airflow.tasks.extract_from_api import extract_data_task


economic_variables = [
    "crypto",
    "forex",
    "stock_prices"
]

@task
def extract_data_task(variable_name:str):
    variables_df = pd.read_csv(f"{BASE_DIR}/mappings/mappings.csv")
    filtered_df = variables_df[variables_df['variable']==variable_name]
    api_key = Variable.get(API_KEY)

    extracted_files = {}
    #it is better to make these api calls in a series rather than in parallel, since we have a limit, and we don't want to overload
    for idx, row in filtered_df.itterrows():
        symbol = row['symbol']
        resolution = row['resolution']
        from_date= row['from']
        to_date = row['to']

        file_path = f'economic_variables/raw_data/{variable_name}/{from_date}_to_{to_date}_{resolution}.csv'

        logging.info(f"Starting extraction process for {variable_name}, {symbol}, {resolution}, {from_date}, {to_date}...")

        #Converting the string date from the csv file into a unix timestamp
        from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
        from_timestamp = from_date_obj.timestamp()

        to_date_obj = datetime.strptime(to_date, '%Y-%m-%d')
        to_timestamp = to_date_obj.timestamp()

        logging.info("Gathering the data from the api...")
        #build the api call
        request = requests.get(
            f"https://finnhub.io/api/v1/{variable_name}/candle?" /
            f"symbol={symbol}&resolution={resolution}&from={from_timestamp}&to={to_timestamp}&token={api_key}")
        file = request.json()

        logging.info("Cleaning the data...")
        # Clean the file
        cleaned_df = clean_file(file)

        logging.info("Uploading data to s3 bucket...")
        save_to_s3(cleaned_df, file_path, ACCESS_KEY, SECRET_KEY)

        logging.info("Extraction finished. Data uploaded to raw data folder in s3.")
        extracted_files.update({variable_name: file_path})

    return extracted_files

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
            extract_data_task(variable)
