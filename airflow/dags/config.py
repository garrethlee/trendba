import os

END_DATE = "2023-05-01T05:30:00+00:00"

AIRFLOW_HOME = os.getenv("AIRFLOW_HOME", "/opt/airflow/")

DATA_DIRECTORY = os.path.join(AIRFLOW_HOME, "data")

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
}
