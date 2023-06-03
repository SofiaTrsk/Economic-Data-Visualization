import os

# All credentials gotten from airflow variables, until I save them to vault
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
API_KEY= "API_KEY"

# S3 bucket credentials
ACCESS_KEY= "s3_bucket_access_key"
SECRET_KEY= "s3_bucket_secret_key"

BUCKET_NAME = 'economic-data-bucket'
USERNAME = 'redshift_username'
PASSWORD = 'redshift_password'
HOST = 'redshift_hostname'
PORT = 'redshift_port'
REDSHIFT_ROLE = 'redshift_role'
DATABASE = 'redshift_database'
ACCOUNT_ID = 'account_id'
TABLE_NAME = 'economic_data'