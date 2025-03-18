from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='etl_kafka_to_datalake',
    default_args=default_args,
    schedule_interval='@hourly',  # tiggers hourly
    start_date=datetime(2024, 1, 1),
    catchup=False,
    description='Kafka data timely ETL -> Data lake',
    tags=['kafka', 'spark', 'datalake']
) as dag:

    extract_task = BashOperator(
        task_id='extract_user_events',
        bash_command='spark-submit /opt/airflow/etl_jobs/extract/preprocessing.py' # Update the script path
    )

    transform_task = BashOperator(
        task_id='transform_events',
        bash_command='spark-submit /opt/airflow/etl_jobs/transform/transform.py' # Update the script path
    )
    
    load_task = BashOperator(
        task_id='transform_events',
        bash_command='spark-submit /opt/airflow/etl_jobs/load/load.py' # Update the script path
    )

    extract_task >>  transform_task >> load_task  # Complete E → T → L pipeline
