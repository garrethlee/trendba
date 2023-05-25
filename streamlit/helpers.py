import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import pytz
import nltk
import re
from wordcloud import WordCloud
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime
import gensim
import numpy as np
from sklearn.manifold import TSNE
from google.cloud import storage
from google.oauth2 import service_account
from io import StringIO


from config import *


def plot_wordcloud(corpus):
    wc = WordCloud(background_color="white", width=600, height=400).generate(
        " ".join(corpus)
    )
    return wc.to_image()


def preprocess_texts(sentences):
    # Convert to lowercase
    sentences = sentences.str.lower()
    # Remove all non-word instances
    sentences = sentences.apply(lambda x: re.sub(r'"', "", str(x)))
    sentences = sentences.apply(lambda x: re.sub(r"\W", " ", str(x)))
    sentences = sentences.apply(lambda x: re.sub(r"[0-9]", " number ", str(x)))
    sentences = sentences.apply(
        lambda x: re.sub(r"\bhttps?:\/\/[^\s]+", " url ", str(x))
    )
    return sentences


def sent_to_words(sentences):
    for sent in sentences:
        yield [word for word in sent.split()]


def preprocess_main_dataframe(df):
    """Process dataframe and create necessary features for visualization

    Args:
        df (DataFrame): Dataframe of 30 subreddits for every hour of the day

    Returns:
        DataFrame: df with newly engineered features
    """
    nltk.download("vader_lexicon", quiet=True)

    # convert UTC to EST
    et_tz = pytz.timezone("US/Eastern")
    df["created_timestamp"] = df["created_timestamp"].apply(
        lambda dt: dt.astimezone(et_tz)
    )
    df["bracket_timestamp"] = df["bracket_timestamp"].apply(
        lambda dt: dt.astimezone(et_tz)
    )

    # Remove URLs
    df["body"] = (
        df["body"]
        .astype(str)
        .apply(lambda doc: re.sub("\[(.*?)\]\((.*?)\)", "\1", doc))
    )

    # Add sentiment scores
    sia = SentimentIntensityAnalyzer()
    df["compound_sentiment"] = df["body"].apply(
        lambda x: sia.polarity_scores(x)["compound"]
    )

    return df


def update_line_chart(df, teams):
    data = df
    mask = data.team.isin(teams)
    fig_hour = px.line(
        data[mask],
        x="bracket_timestamp",
        y="score",
        color="team",
        color_discrete_sequence=[
            color for team, color in NBA_TEAMS_COLORS.items() if team in teams
        ],
        custom_data=["team"],
        range_y=[0, 500],
        range_x=[
            data.bracket_timestamp.min(),
            data.bracket_timestamp.max(),
        ],
        title="Number of Posts per hour",
    )
    fig_hour.update_traces(
        hovertemplate="""<b>%{customdata[0]}</b> <br>%{x} <br>%{y} posts<extra></extra>""",
        line=dict(width=3),
    )

    return fig_hour


def update_bar_chart(df, teams):
    """Create bar chart for sentiments of each NBA subreddit

    Args:
        df (DataFrame): A dataframe consisting `bracket_timestamp`, `team`, and `compound_sentiment` scores for each team in each time bracket

    Returns:
        px.Figure : returns a plotly express figure
    """

    df = preprocess_sentiments(df)
    mask = df.team.isin(teams)

    fig = px.bar(
        df[mask],
        y="team",
        x="compound_sentiment",
        color="team",
        color_discrete_sequence=[
            color for team, color in NBA_TEAMS_COLORS.items() if team in teams
        ],
        barmode="relative",
        animation_frame="bracket_timestamp",
        animation_group="team",
        range_x=[-0.3, 0.5],
        title="Average Sentiment per Team Subreddit",
        orientation="h",
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Sentiment",
        sliders=[
            dict(
                active=0,
                yanchor="top",
                xanchor="left",
                currentvalue=dict(
                    font=dict(size=15), prefix="", visible=True, xanchor="right"
                ),
                transition=dict(duration=1000, easing="linear"),
                # pad=dict(b=10, t=200),
                len=0.9,
                x=0.1,
                y=0,
            )
        ],
        updatemenus=[
            dict(
                type="buttons",
                buttons=[
                    dict(
                        label="Play",
                        method="animate",
                        args=[
                            None,
                            {
                                "frame": {"duration": 500, "redraw": True},
                                "fromcurrent": True,
                            },
                        ],
                    ),
                    dict(
                        label="Pause",
                        method="animate",
                        args=[
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": False},
                                "mode": "immediate",
                            },
                        ],
                    ),
                ],
                direction="left",
                # pad={"l": 50, "t": 200},
                showactive=False,
                x=0.1,
                xanchor="right",
                y=0.1,
                yanchor="top",
            )
        ],
    )

    fig.update_traces(hovertemplate="<b>%{x}</b> <br>%{y}<extra></extra>")

    for i, frame in enumerate(fig.frames):
        for j, bar in enumerate(frame.data):
            fig.frames[i].data[j].hovertemplate = "<b>%{x}</b> <br>%{y}<extra></extra>"

    return fig


def preprocess_sentiments(df):
    # Add sentiment = 0 for missing entries
    for ts in df.bracket_timestamp.unique():
        for te in df.team.unique():
            if df.query("bracket_timestamp == @ts & team == @te").empty:
                new_row = {
                    "bracket_timestamp": [ts],
                    "team": [te],
                    "compound_sentiment": [0],
                }
                df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=True)

    df = df.sort_values(by=["bracket_timestamp", "team"])
    df["bracket_hour"] = df["bracket_timestamp"].dt.hour
    df["bracket_timestamp"] = df["bracket_timestamp"].apply(
        lambda x: datetime.strftime(x, "%B %d, %H:%M")
    )
    return df


def generate_tsne(tokens, body, team):
    # Create Dictionary
    id2word = gensim.corpora.Dictionary(tokens)
    # Create Corpus
    texts = tokens
    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]
    # number of topics
    num_topics = 5
    # Build LDA model
    lda_model = gensim.models.LdaModel(
        corpus=corpus, id2word=id2word, num_topics=num_topics, passes=1
    )

    # Get topic weights
    topic_weights = []
    for i, row_list in enumerate(lda_model[corpus]):
        topic_weights.append([w for _, w in row_list])

    # Array of topic weights
    arr = pd.DataFrame(topic_weights).fillna(0).values

    # Dominant topic number in each doc
    topic_num = np.argmax(arr, axis=1)
    topic_num = [f"Topic {n}" for n in topic_num]

    # tSNE Dimension Reduction
    tsne_model = TSNE(n_components=2, verbose=0, random_state=0, angle=0.99, init="pca")
    tsne_lda = tsne_model.fit_transform(arr)
    tsne_lda = pd.DataFrame(np.c_[tsne_lda, topic_num, body])

    # Plot the Topic Clusters
    fig = px.scatter(
        x=tsne_lda[0],
        y=tsne_lda[1],
        color=tsne_lda[2],
        custom_data=[tsne_lda[3]],
        width=600,
        height=600,
        title=f"Topic Distribution for the {team} subreddit",
    )
    fig.update_traces(hovertemplate="%{customdata[0]}<extra></extra>")
    return fig


def get_data(date_obj):
    date = date_obj.strftime("%Y-%m-%d")
    credentials = service_account.Credentials.from_service_account_file(
        "credentials/data-service-account.json"
    )
    client = storage.Client(credentials=credentials, project=credentials.project_id)
    bucket = client.bucket("trendba-bucket-1")
    blob = bucket.blob(blob_name=f"output/{date}.csv")
    string = StringIO(blob.download_as_text())
    df = pd.read_csv(string, parse_dates=[0, 1])
    return df
