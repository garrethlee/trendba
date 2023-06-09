import pandas as pd
from datetime import datetime
from helpers import *


#######

# Starting configs
PICKED_TEAMS = ["Los Angeles Lakers", "Golden State Warriors"]

NBA_TEAMS = [
    "Atlanta Hawks",
    "Boston Celtics",
    "Brooklyn Nets",
    "Charlotte Hornets",
    "Chicago Bulls",
    "Cleveland Cavaliers",
    "Dallas Mavericks",
    "Denver Nuggets",
    "Detroit Pistons",
    "Golden State Warriors",
    "Houston Rockets",
    "Indiana Pacers",
    "Los Angeles Clippers",
    "Los Angeles Lakers",
    "Memphis Grizzlies",
    "Miami Heat",
    "Milwaukee Bucks",
    "Minnesota Timberwolves",
    "New Orleans Pelicans",
    "New York Knicks",
    "Oklahoma City Thunder",
    "Orlando Magic",
    "Philadelphia 76ers",
    "Phoenix Suns",
    "Portland Trail Blazers",
    "Sacramento Kings",
    "San Antonio Spurs",
    "Toronto Raptors",
    "Utah Jazz",
    "Washington Wizards",
    "NBA",
]

NBA_TEAMS_COLORS = {
    "Atlanta Hawks": "#E03A3E",
    "Boston Celtics": "#008348",
    "Brooklyn Nets": "#000000",
    "Charlotte Hornets": "#00788C",
    "Chicago Bulls": "#CE1141",
    "Cleveland Cavaliers": "#860038",
    "Dallas Mavericks": "#00538C",
    "Denver Nuggets": "#4D90CD",
    "Detroit Pistons": "#C8102E",
    "Golden State Warriors": "#1D428A",
    "Houston Rockets": "#CE1141",
    "Indiana Pacers": "#002D62",
    "Los Angeles Clippers": "#C8102E",
    "Los Angeles Lakers": "#552583",
    "Memphis Grizzlies": "#5D76A9",
    "Miami Heat": "#98002E",
    "Milwaukee Bucks": "#00471B",
    "Minnesota Timberwolves": "#0C2340",
    "New Orleans Pelicans": "#0C2340",
    "New York Knicks": "#F58426",
    "Oklahoma City Thunder": "#007AC1",
    "Orlando Magic": "#0077C0",
    "Philadelphia 76ers": "#006BB6",
    "Phoenix Suns": "#1D1160",
    "Portland Trail Blazers": "#E03A3E",
    "Sacramento Kings": "#5A2D81",
    "San Antonio Spurs": "#000000",
    "Toronto Raptors": "#CE1141",
    "Utah Jazz": "#002B5C",
    "Washington Wizards": "#E31837",
    "NBA": "#000000",
}

STOPWORDS = [
    "i",
    "me",
    "my",
    "myself",
    "we",
    "our",
    "ours",
    "ourselves",
    "you",
    "youre",
    "youve",
    "youll",
    "youd",
    "your",
    "yours",
    "yourself",
    "yourselves",
    "he",
    "him",
    "his",
    "himself",
    "she",
    "shes",
    "her",
    "hers",
    "herself",
    "it",
    "its",
    "its",
    "itself",
    "they",
    "them",
    "their",
    "theirs",
    "themselves",
    "what",
    "which",
    "who",
    "whom",
    "this",
    "that",
    "thatll",
    "these",
    "those",
    "am",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "having",
    "do",
    "does",
    "did",
    "doing",
    "a",
    "an",
    "the",
    "and",
    "but",
    "if",
    "or",
    "because",
    "as",
    "until",
    "while",
    "of",
    "at",
    "by",
    "for",
    "with",
    "about",
    "against",
    "between",
    "into",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "to",
    "from",
    "up",
    "down",
    "in",
    "out",
    "on",
    "off",
    "over",
    "under",
    "again",
    "further",
    "then",
    "once",
    "here",
    "there",
    "when",
    "where",
    "why",
    "how",
    "all",
    "any",
    "both",
    "each",
    "few",
    "more",
    "most",
    "other",
    "some",
    "such",
    "no",
    "nor",
    "not",
    "only",
    "own",
    "same",
    "so",
    "than",
    "too",
    "very",
    "s",
    "t",
    "can",
    "will",
    "just",
    "don",
    "dont",
    "should",
    "shouldve",
    "now",
    "d",
    "ll",
    "m",
    "o",
    "re",
    "ve",
    "y",
    "ain",
    "aren",
    "arent",
    "couldn",
    "couldnt",
    "didn",
    "didnt",
    "doesn",
    "doesnt",
    "hadn",
    "hadnt",
    "hasn",
    "hasnt",
    "haven",
    "havent",
    "isn",
    "isnt",
    "ma",
    "mightn",
    "mightnt",
    "mustn",
    "mustnt",
    "needn",
    "neednt",
    "shan",
    "shant",
    "shouldn",
    "shouldnt",
    "wasn",
    "wasnt",
    "weren",
    "werent",
    "won",
    "wont",
    "wouldn",
    "wouldnt",
    "would",
    "said",
    "number",
    "get",
    "way",
    "like",
    "could",
    "url",
    "even",
    "team",
    "one",
    "think",
    "play",
    "really",
    "pjpg",
    "jpeg",
    "jpg",
    "gif",
    "us",
    "game",
    "got",
    "back",
    "lol",
    "lmao",
    "need",
    "people",
    "go",
    "know",
    "https",
    "going",
    "also",
    "last",
    "giphy",
    "com",
]
