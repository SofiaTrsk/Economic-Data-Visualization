import os

# All credentials gotten from airflow variables, until I save them to vault
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
API_KEY= "finnhub_api_key"

# S3 bucket credentials
ACCESS_KEY= "access_key"
SECRET_KEY= "secret_key"

BUCKET_NAME = 'economic-variables-bucket'
USERNAME = 'redshift_username'
PASSWORD = 'redshift_password'
HOST = 'redshift_hostname'
PORT = 'redshift_port'
REDSHIFT_ROLE = 'redshift_role'
DATABASE = 'redshift_database'
ACCOUNT_ID = 'account_id'
TABLE_NAME = 'economic_data'