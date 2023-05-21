import os

# All credentials gotten from airflow variables, until I save them to vault
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
API_KEY= "finnhub_api_key"

# S3 bucket credentials
ACCESS_KEY= "access_key"
SECRET_KEY= "secret_key"