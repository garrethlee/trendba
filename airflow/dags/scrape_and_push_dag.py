from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

import itertools

from config import *
from helpers import *

scrape_dag = DAG(
    dag_id="scrape_and_save_to_csv",
    description="Workflow to scrape Reddit data on NBA teams using the Python Wrapper for the Reddit API and save to csv files",
    schedule="0 * * * *",
    catchup=False,
    start_date=datetime(2023, 5, 13),
)


with scrape_dag:
    scraping_thread_a = PythonOperator(
        task_id="scrape_teams_1-8",
        python_callable=scrape_and_save,
        op_args=[dict(itertools.islice(TEAMS.items(), 0, 8)), "{{ execution_date }}"],
        provide_context=True,
    )
    scraping_thread_b = PythonOperator(
        task_id="scrape_teams_9-16",
        python_callable=scrape_and_save,
        op_args=[dict(itertools.islice(TEAMS.items(), 8, 16)), "{{ execution_date }}"],
        provide_context=True,
    )
    scraping_thread_c = PythonOperator(
        task_id="scrape_teams_17-24",
        python_callable=scrape_and_save,
        op_args=[dict(itertools.islice(TEAMS.items(), 16, 24)), "{{ execution_date }}"],
        provide_context=True,
    )
    scraping_thread_d = PythonOperator(
        task_id="scrape_teams_25-30",
        python_callable=scrape_and_save,
        op_args=[dict(itertools.islice(TEAMS.items(), 24, 31)), "{{ execution_date }}"],
        provide_context=True,
    )

    join_csv = PythonOperator(task_id="join_csv", python_callable=join)

    push_to_bigquery = PythonOperator(
        task_id="push_csv_to_cloud_storage",
        python_callable=push_to_gcs,
        op_kwargs=dict(
            source_file_name=f"{AIRFLOW_DATA_DIRECTORY}/all_teams.csv",
            destination_blob_name="data/reddit-nba-scrape-job/{{ execution_date | ds }}/{{ execution_date }}.csv",
            project_id=GOOGLE_PROJECT_ID,
            bucket_name=GOOGLE_BUCKET_NAME,
        ),
    )

    trigger_bigquery_table_dag = TriggerDagRunOperator(
        task_id="trigger_push_to_bq", trigger_dag_id="cloud_storage_to_bigquery_dag"
    )

    # Workflow
    (
        [scraping_thread_a, scraping_thread_b, scraping_thread_c, scraping_thread_d]
        >> join_csv
        >> push_to_bigquery
        >> trigger_bigquery_table_dag
    )
