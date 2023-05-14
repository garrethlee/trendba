import os

REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AIRFLOW_HOME = os.getenv("AIRFLOW_HOME", "/opt/airflow/")
AIRFLOW_DATA_DIRECTORY = os.path.join(AIRFLOW_HOME, "data")

GOOGLE_BUCKET_NAME = "trendba-bucket-1"
GOOGLE_PROJECT_ID = "trendba"
GOOGLE_DATASET_NAME = "all_subreddits_daily"

TEAMS = {
    "Atlanta Hawks": "AtlantaHawks",
    "Boston Celtics": "bostonceltics",
    "Brooklyn Nets": "gonets",
    "Charlotte Hornets": "CharlotteHornets",
    "Chicago Bulls": "chicagobulls",
    "Cleveland Cavaliers": "clevelandcavs",
    "Dallas Mavericks": "Mavericks",
    "Denver Nuggets": "denvernuggets",
    "Detroit Pistons": "DetroitPistons",
    "Golden State Warriors": "warriors",
    "Houston Rockets": "rockets",
    "Indiana Pacers": "pacers",
    "Los Angeles Clippers": "LAClippers",
    "Los Angeles Lakers": "lakers",
    "Memphis Grizzlies": "memphisgrizzlies",
    "Miami Heat": "heat",
    "Milwaukee Bucks": "MkeBucks",
    "Minnesota Timberwolves": "timberwolves",
    "New Orleans Pelicans": "NOLAPelicans",
    "New York Knicks": "nyknicks",
    "Oklahoma City Thunder": "Thunder",
    "Orlando Magic": "OrlandoMagic",
    "Philadelphia 76ers": "sixers",
    "Phoenix Suns": "suns",
    "Portland Trail Blazers": "ripcity",
    "Sacramento Kings": "kings",
    "San Antonio Spurs": "NBASpurs",
    "Toronto Raptors": "torontoraptors",
    "Utah Jazz": "UtahJazz",
    "Washington Wizards": "washingtonwizards",
    # Include the r/nba subreddit
    "NBA": "nba",
}
