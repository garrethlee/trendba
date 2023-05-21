from config import *
from helpers import *
from datetime import datetime, timedelta

# STORE WORDCLOUDS
WORDCLOUDS = {}

try:
    today = datetime.today().date()
    df = get_data(today)
except Exception as e:
    df = get_data(today - timedelta(days=1))

DAILY_DATA_DF = preprocess_main_dataframe(df)

# AGGREGATIONS FROM DAILY_DATA_DF
HOURLY_POSTS_DF = (
    DAILY_DATA_DF.groupby(["bracket_timestamp", "team"]).score.count().reset_index()
)

AVERAGE_SENTIMENT_DF = (
    DAILY_DATA_DF.groupby(["bracket_timestamp", "team"])
    .compound_sentiment.mean()
    .reset_index()
)
