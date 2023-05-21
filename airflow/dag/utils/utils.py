import io

import boto3
import pandas as pd

economic_variables = [
    "CRYPTO_CANDLES",
    "FOREX_CANDLES",
    "STOCK_PRICE_CANDLES"
]

BUCKET_NAME = 'economic-variables-bucket'


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