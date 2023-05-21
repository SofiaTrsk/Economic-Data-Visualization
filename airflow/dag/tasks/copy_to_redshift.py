from airflow.dag.utils.utils import load_data_into_redshift, connect_to_redshift
from airflow.decorators import task


# ToDo: Find another way to get the data from the s3 bucket. Possibly write a method. Redshift db to be removed later if it is possible to get files directly from s3
@task
def copy_to_redshift():
    rs_conn = connect_to_redshift()
    load_data_into_redshift(rs_conn)