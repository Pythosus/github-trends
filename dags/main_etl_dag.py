from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import task
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from src.get_trends import *
from src.search_keywords import readme_text, extract_keywords
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
def extract_info(**context) -> str:
    repos = get_github_trends()

    ds = context['ds']
    file_key = f'raw/{ds}.json'
    json_bytes = json.dumps(repos[i], indent=2).encode('utf-8')

    try:
        s3_client.create_bucket(Bucket=bucket)
    except ClientError as e:
        if e.response['Error']['Code'] != 'BucketAlreadyOwned':
            raise


    s3_client.put_object(
        Bucket=bucket,
        Key=file_key,
        Body=json_bytes,
        ContentType='application/json'
    )
    return file_key

@task(task_id='add_keywords')
def transform_info(key: str):
    response = s3_client.get_object(Bucket=bucket, Key=key)
    raw_bytes = response["Body"].read()
    repos = list(json.loads(raw_bytes.decode("utf-8")))
    for repo in repos:
        readme = readme_text(repo['url'])
        keysANDscores = extract_keywords(readme, repo['topics'])

with DAG(
    'main data trends dag',
    default_args=default_args,
    description='extract github trends, load to db, find top technologies, load result',
    schedule_interval='@daily',
    catchup=False,
    tags=['IT trends', 'GitHub', 'Эщкере)'],
) as dag:
    pass
