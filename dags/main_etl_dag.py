from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import task
from datetime import datetime, timedelta
from src.get_trends import *
from src.search_keywords import *
import boto3, json
from botocore.exceptions import ClientError

s3_client = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="admin",
    aws_secret_access_key="admin12345",
)


default_args = {
    'owner' : 'fed0',
    'depends_on_past' : False,
    'retries' : 1,
    'retry_delay': timedelta(minutes=1),
    'start_date': datetime.now()
}

bucket = 'bufer'

@task(task_id='extract_info')
def extract_info() -> int:
    repos = get_github_trends()

    try:
        s3_client.create_bucket(Bucket=bucket)
    except ClientError as e:
        if e.response['Error']['Code'] != 'BucketAlreadyOwnedByYou':
            raise

    for i in range(len(repos)):
        json_bytes = json.dumps(repos[i], indent=4).encode('utf-8')
        file_key = f'bronze/{i}_{datetime.now().strftime("%d.%m.%Y")}.json'

        s3_client.put_object(
            Bucket=bucket,
            Key=file_key,
            Body=json_bytes,
            ContentType='application/json'
        )
    return len(repos)

@task(task_id='add_keywords')
def transform_info(ln: int):
    pass

with DAG(
    'main data trends dag',
    default_args=default_args,
    description='extract github trends, load to db, find top technologies, load result',
    schedule_interval='@daily',
    catchup=False,
    tags=['extract IT trends', 'GitHub', 'Эщкере)'],
) as dag:
    pass
