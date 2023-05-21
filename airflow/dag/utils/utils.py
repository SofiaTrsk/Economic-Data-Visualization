import io
import sys

import boto3
import pandas as pd
from sqlalchemy_utils.types.pg_composite import psycopg2

from psycopg2 import sql

from airflow.dag.configs.configs import DATABASE, USERNAME, PASSWORD, HOST, PORT, BUCKET_NAME, TABLE_NAME, ACCOUNT_ID, \
    REDSHIFT_ROLE

economic_variables = [
    "crypto",
    "forex",
    "stock_prices"
]

# ToDo: Fix the way we're getting the path
file_path = f"s3://{BUCKET_NAME}/economic_variables/raw_data"
role_string = f"arn:aws:iam::{ACCOUNT_ID}:role/{REDSHIFT_ROLE}"


sql_create_table = sql.SQL(
    """CREATE TABLE IF NOT EXISTS {table} (
                            id varchar PRIMARY KEY,
                            o float,
                            c float,
                            h float,
                            l float,
                            y date,
                            url varchar(max),
                            upvote_ratio float,
                            over_18 bool,
                            edited bool,
                            spoiler bool,
                            stickied bool
                        );"""
).format(table=sql.Identifier(TABLE_NAME))

create_temp_table = sql.SQL(
    "CREATE TEMP TABLE staging_table (LIKE {table});"
).format(table=sql.Identifier(TABLE_NAME))
sql_copy_to_temp = f"COPY staging_table FROM '{file_path}' iam_role '{role_string}' IGNOREHEADER 1 DELIMITER ',' CSV;"
delete_from_table = sql.SQL(
    "DELETE FROM {table} USING staging_table WHERE {table}.id = staging_table.id;"
).format(table=sql.Identifier(TABLE_NAME))
insert_into_table = sql.SQL(
    "INSERT INTO {table} SELECT * FROM staging_table;"
).format(table=sql.Identifier(TABLE_NAME))
drop_temp_table = "DROP TABLE staging_table;"

def save_to_s3(pd_df, file_path, access_key, secret_key):
    csv_buffer = io.StringIO()
    csv_data = pd_df.to_csv(csv_buffer, index=False)
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    s3.put_object(Body=csv_data, Bucket=BUCKET_NAME, Key=file_path)


def clean_file(df):
    df.drop(df['v'], axis=1, inplace=True)
    df.dropna(axis=0, inplace=True)

    # We get the date column as unix timestamps from the api call. We have to convert it again
    df['t'] = pd.to_datetime(df['t'], unit='s')

    return df

def connect_to_redshift():
    """Connect to Redshift instance"""
    try:
        rs_conn = psycopg2.connect(
            dbname=DATABASE, user=USERNAME, password=PASSWORD, host=HOST, port=PORT
        )
        return rs_conn
    except Exception as e:
        print(f"Unable to connect to Redshift. Error {e}")
        sys.exit(1)


def load_data_into_redshift(rs_conn):
    """Load data from S3 into Redshift"""
    with rs_conn:

        cur = rs_conn.cursor()
        cur.execute(sql_create_table)
        cur.execute(create_temp_table)
        cur.execute(sql_copy_to_temp)
        cur.execute(delete_from_table)
        cur.execute(insert_into_table)
        cur.execute(drop_temp_table)

        # Commit only at the end, so we won't end up
        # with a temp table and deleted main table if something fails
        rs_conn.commit()