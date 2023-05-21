from airflow import DAG
from airflow.providers.google.cloud.transfers.bigquery_to_gcs import (
    BigQueryToGCSOperator,
)
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

from datetime import datetime

from config import *
from helpers import *


CREATE_NATIVE_TABLE_QUERY = (
    f"CREATE OR REPLACE TABLE `{GOOGLE_DATASET_NAME}.native_table_"
    + "{{execution_date | ds }}`"
    + " AS "
    + f"SELECT * FROM `{GOOGLE_DATASET_NAME}.external_table_"
    + "{{execution_date | ds }}`"
)


store_daily_dag = DAG(
    dag_id="store_daily_csv_in_gcs",
    description="Store data scraped so far in a csv file in cloud storage",
    schedule="0 * * * *",
    catchup=False,
    start_date=datetime(2023, 5, 13),
)

# Create an external table
with store_daily_dag:
    create_table = BigQueryInsertJobOperator(
        task_id="create_native_table",
        configuration=dict(
            query=dict(query=CREATE_NATIVE_TABLE_QUERY, useLegacySql=False)
        ),
        location="us-west1",
    )

    store_to_gcs = BigQueryToGCSOperator(
        task_id="store_to_gcs",
        source_project_dataset_table=f"{GOOGLE_PROJECT_ID}.{GOOGLE_DATASET_NAME}.native_table_"
        + "{{ execution_date | ds }}",
        destination_cloud_storage_uris=[
            f"gs://{GOOGLE_BUCKET_NAME}/output/" + "{{ execution_date | ds }}.csv"
        ],
    )

    create_table >> store_to_gcs
