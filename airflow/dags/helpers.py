from config import *

from datetime import datetime, timedelta
import os
import time
import re
import logging
import pandas as pd
import praw

from google.cloud import storage

storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB


def push_to_gcs(
    source_file_name: str, destination_blob_name: str, project_id: str, bucket_name: str
):
    """Pushes all_teams.csv to google cloud storage

    Args:
        source_file_name (str): The source csv filename
        destination_blob_name (str): Destination blob name
        project_id (str): GCP Project ID
        bucket_name (str): Google Cloud Storage Bucket Name
    """

    storage_client = storage.Client(project=project_id)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(
        f"File {source_file_name} has been uploaded to Google Cloud Storage Bucket {bucket_name}"
    )


def scrape_and_save(teams: dict, current_date: str, **kwargs):
    """Scrape NBA data from PushShift based on teams' subreddits, then saves it
    onto a csv file

    Args:
        teams (dict): Dictionary of (NBA team, Subreddit URL) to scrape
        current_date (str): Current date of airflow job
    """

    import praw

    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        password=REDDIT_PASSWORD,
        username=REDDIT_USERNAME,
        user_agent=REDDIT_USERNAME,
    )

    # Preliminary calculation for hours
    curr_date = datetime.fromisoformat(current_date)
    curr_date = curr_date.replace(tzinfo=None)
    minimum_timestamp = curr_date - timedelta(hours=1)

    teams_df = pd.DataFrame()

    if not os.path.exists(AIRFLOW_DATA_DIRECTORY):
        os.makedirs(AIRFLOW_DATA_DIRECTORY)

    for team in teams:
        retries = 10
        while retries >= 0:
            try:
                subreddit = reddit.subreddit(teams[team])

                # Get the latest posts in the subreddit within the current hour
                latest_posts = subreddit.comments(limit=500)

                for post in latest_posts:
                    created_date = datetime.fromtimestamp(post.created_utc)

                    if created_date > curr_date:
                        continue
                    if created_date < minimum_timestamp:
                        break
                    df = pd.DataFrame(
                        {
                            "created_timestamp": [created_date],
                            "bracket_timestamp": [
                                created_date.replace(minute=0, second=0, microsecond=0)
                            ],
                            "team": [team],
                            "subreddit": [teams[team]],
                            "score": [post.score],
                            "body": [post.body],
                        },
                        index=None,
                    )
                    teams_df = pd.concat([teams_df, df])

                logging.info(f"{team}: Successfully scraped!")
                break

            except Exception as e:
                retries -= 1
                logging.error(e)
                logging.error(f"Retrying! {retries} attempts before skipping!")
                time.sleep(1)

    teams_df.to_csv(
        f"{AIRFLOW_DATA_DIRECTORY}/output_{kwargs['ti'].task_id}.csv",
        mode="w",
        index=False,
    )

    logging.info(f"Saved in {AIRFLOW_DATA_DIRECTORY}/output_{kwargs['ti'].task_id}.csv")


def join():
    """Joins all individual scraping csv files into one csv file"""
    df = pd.concat(
        [
            pd.read_csv(f"{AIRFLOW_DATA_DIRECTORY}/output_scrape_teams_1-8.csv"),
            pd.read_csv(f"{AIRFLOW_DATA_DIRECTORY}/output_scrape_teams_9-16.csv"),
            pd.read_csv(f"{AIRFLOW_DATA_DIRECTORY}/output_scrape_teams_17-24.csv"),
            pd.read_csv(f"{AIRFLOW_DATA_DIRECTORY}/output_scrape_teams_25-30.csv"),
        ]
    )
    df.to_csv(f"{AIRFLOW_DATA_DIRECTORY}/all_teams.csv", index=False, mode="w")
