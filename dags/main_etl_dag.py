import os
from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import boto3, json
from botocore.exceptions import ClientError
import psycopg2

from src.get_trends import get_github_trends
from src.search_keywords import readme_text, extract_keywords
from src.config import get_s3_client, get_pg_connection, bucket


default_args = {
    'owner' : 'fed0',
    'depends_on_past' : False,
    'retries' : 1,
    'retry_delay': timedelta(minutes=1),
    'start_date': datetime.now()
}


@task(task_id='extract_info')
def extract_info(**context) -> str:
    repos = get_github_trends()

    s3_client = get_s3_client()

    ds = context['ds']
    file_key = f'raw/{ds}.json'
    json_bytes = json.dumps(repos, indent=2).encode('utf-8')

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
    print(file_key)
    return file_key


@task(task_id='add_keywords')
def transform_info(key: str, **context):
    s3_client = get_s3_client()

    response = s3_client.get_object(Bucket=bucket, Key=key)
    raw_bytes = response["Body"].read()
    repos = list(json.loads(raw_bytes.decode("utf-8")))
    for repo in repos:
        readme = readme_text(repo['raw_readme_url'])
        keysANDscores = extract_keywords(readme, repo['topics'])
        repo['keywords'] = keysANDscores
    
    ds = context['ds']
    file_key = f'medium/{ds}.json'
    json_bytes = json.dumps(repos, indent=2).encode('utf-8')

    s3_client.put_object(
            Bucket=bucket,
            Key=file_key,
            Body=json_bytes,
            ContentType='application/json'
        )
    return file_key



@task(task_id='load_trends_info')
def load_trends(file: str):
    s3_client = get_s3_client()
    
    response = s3_client.get_object(Bucket=bucket, Key=file)
    raw_bytes = response["Body"].read()
    repos = list(json.loads(raw_bytes.decode("utf-8")))

    print(repos)

    conn = psycopg2.connect(get_pg_connection())

    cur = conn.cursor()
    for repo in repos:
        query = '''INSERT INTO repositories(name_rep, stars, description)
        VALUES(%s, %s, %s)
        RETURNING id_rep'''
        cur.execute(query, (repo['name'], repo['stars'], repo['description']))
        id_rep = cur.fetchone()[0]
        for x in repo['keywords']:
            for word, score in x.items():
                query_k = f'''INSERT INTO keywords(id_rep, tech, score)
                VALUES (%s, %s, %s)'''
                cur.execute(query_k, (id_rep, word, score))
    conn.commit()
    cur.close()
    conn.close()

with DAG(
    'main_data_trends_dag',
    default_args=default_args,
    description='extract github trends, load to db, find top technologies, load result',
    schedule_interval='@daily',
    catchup=False,
    tags=['IT trends', 'GitHub', 'Эщкере)'],
) as dag:
    raw = extract_info()
    transformed = transform_info(raw)
    load = load_trends(transformed)

    raw >> transformed >> load
