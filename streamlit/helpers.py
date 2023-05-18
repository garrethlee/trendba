import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz
import re
from wordcloud import WordCloud
from nltk.sentiment import SentimentIntensityAnalyzer

from config import *


def preprocess_main_dataframe(df):
    """Process dataframe and create necessary features for visualization

    Args:
        df (DataFrame): Dataframe of 30 subreddits for every hour of the day

    Returns:
        DataFrame: df with newly engineered features
    """
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


# def create_subreddit_sentiment_figure(df):
#     """Create bar chart for sentiments of each NBA subreddit

#     Args:
#         df (DataFrame): A dataframe consisting `bracket_timestamp`, `team`, and `compound_sentiment` scores for each team in each time bracket

#     Returns:
#         px.Figure : returns a plotly express figure
#     """

#     df = preprocess_sentiments(df)

#     fig = px.bar(
#         df,
#         x="team",
#         y="compound_sentiment",
#         color="team",
#         color_discrete_sequence=list(NBA_TEAMS_COLORS.values()),
#         barmode="relative",
#         animation_frame="bracket_timestamp",
#         animation_group="team",
#         range_y=[-0.3, 0.5],
#         title="Average Sentiment per Team Subreddit",
#     )

#     fig.update_layout(
#         xaxis_title=None,
#         yaxis_title="Sentiment",
#         sliders=[
#             dict(
#                 active=0,
#                 yanchor="top",
#                 xanchor="left",
#                 currentvalue=dict(
#                     font=dict(size=15), prefix="", visible=True, xanchor="right"
#                 ),
#                 transition=dict(duration=1000, easing="linear"),
#                 pad=dict(b=10, t=200),
#                 len=0.9,
#                 x=0.1,
#                 y=0,
#             )
#         ],
#         updatemenus=[
#             dict(
#                 type="buttons",
#                 buttons=[
#                     dict(
#                         label="Play",
#                         method="animate",
#                         args=[
#                             None,
#                             {
#                                 "frame": {"duration": 500, "redraw": True},
#                                 "fromcurrent": True,
#                             },
#                         ],
#                     ),
#                     dict(
#                         label="Pause",
#                         method="animate",
#                         args=[
#                             [None],
#                             {
#                                 "frame": {"duration": 0, "redraw": False},
#                                 "mode": "immediate",
#                             },
#                         ],
#                     ),
#                 ],
#                 direction="left",
#                 pad={"l": 50, "t": 200},
#                 showactive=False,
#                 x=0.1,
#                 xanchor="right",
#                 y=0.1,
#                 yanchor="top",
#             )
#         ],
#     )

#     fig.update_traces(hovertemplate="<b>%{x}</b> <br>%{y}<extra></extra>")

#     for i, frame in enumerate(fig.frames):
#         for j, bar in enumerate(frame.data):
#             fig.frames[i].data[j].hovertemplate = "<b>%{x}</b> <br>%{y}<extra></extra>"

#     return fig


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
                pad={"l": 50, "t": 200},
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
