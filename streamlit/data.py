from config import *
from helpers import *

# STORE WORDCLOUDS
WORDCLOUDS = {}

DAILY_DATA_DF = preprocess_main_dataframe(
    pd.read_csv(DAILY_DATA_CSV_PATH, parse_dates=[0, 1])
)

# AGGREGATIONS FROM DAILY_DATA_DF
HOURLY_POSTS_DF = (
    DAILY_DATA_DF.groupby(["bracket_timestamp", "team"]).score.count().reset_index()
)

AVERAGE_SENTIMENT_DF = (
    DAILY_DATA_DF.groupby(["bracket_timestamp", "team"])
    .compound_sentiment.mean()
    .reset_index()
)
