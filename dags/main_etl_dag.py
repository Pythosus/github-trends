from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner' : 'fed0',
    'depends_on_past' : False,
    'retries' : 1,
    'retry_delay': timedelta(minutes=1),
    'start_date': datetime.now()
}

with DAG(
    'main data trends dag',
    default_args=default_args,
    description='extract github trends, load to db, find top technologies, load result',
    schedule_interval='@dayly',
    catchup=False,
    tags=['extract IT trends', 'GitHub', 'Эщкере)'],
) as dag:
    pass
