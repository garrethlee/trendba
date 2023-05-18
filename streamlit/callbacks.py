from dash import Output, Input
import plotly.express as px

from helpers import *
from config import *
from data import *


def get_callbacks(app):
    @app.callback(
        Output("posts_per_hour_graph", "figure"),
        Output("sentiment_graph", "figure"),
        Input("posts_per_hour_checklist", "value"),
    )
    def update_charts(teams):
        fig_hour = update_line_chart(HOURLY_POSTS_DF, teams)
        fig_sentiment = update_bar_chart(AVERAGE_SENTIMENT_DF, teams)
        return fig_hour, fig_sentiment
