import os
import boto3

s3_endpoint = os.getenv("AWS_ENDPOINT_URL", "http://localhost:9000")
s3_access_key = os.getenv("AWS_ACCESS_KEY_ID", "admin")
s3_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY", "admin12345")
bucket = 'bufer'

pg_host = os.getenv("PG_HOST", "main_db")       
pg_port = int(os.getenv("PG_PORT", "5432"))     
pg_user = os.getenv("PG_USER", "postgre")
pg_password = os.getenv("PG_PASSWORD", "postgre")
pg_dbname = os.getenv("PG_DBNAME", "github_trends")

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=s3_endpoint,
        aws_access_key_id=s3_access_key,
        aws_secret_access_key=s3_secret_key,
    )

def get_pg_connection():
    return f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_dbname}"