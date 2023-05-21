from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateExternalTableOperator,
)
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

from config import *
from helpers import *


bigquery_dag = DAG(
    dag_id="cloud_storage_to_bigquery_dag",
    description="Workflow to push cloud storage objects to bigquery",
    schedule="0 * * * *",
    catchup=False,
    start_date=datetime(2023, 5, 13),
)

# Create an external table
with bigquery_dag:
    create_external_table = BigQueryCreateExternalTableOperator(
        task_id="create_bq_external_table",
        bucket=GOOGLE_BUCKET_NAME,
        table_resource={
            "tableReference": {
                "projectId": GOOGLE_PROJECT_ID,
                "datasetId": GOOGLE_DATASET_NAME,
                "tableId": "external_table_{{ execution_date | ds }}",
            },
            "externalDataConfiguration": {
                "autodetect": True,
                "sourceFormat": "CSV",
                "sourceUris": [
                    f"gs://{GOOGLE_BUCKET_NAME}/data/reddit-nba-scrape-job/"
                    + "{{ execution_date | ds }}/*.csv"
                ],
                # Take care of quotes
                "csvOptions": {
                    "skipLeadingRows": "1",
                    "allowQuotedNewlines": True,
                    "allowJaggedRows": True,
                },
                "location": "us-west1",
            },
        },
    )

    trigger_native_table_dag = TriggerDagRunOperator(
        task_id="trigger_create_native_table", trigger_dag_id="store_daily_csv_in_gcs"
    )

    create_external_table >> trigger_native_table_dag
