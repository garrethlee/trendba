from dash import Output, Input, dcc, html, ctx
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from io import BytesIO
import base64

from helpers import *
from config import *
from data import HOURLY_POSTS_DF, AVERAGE_SENTIMENT_DF, DAILY_DATA_DF, WORDCLOUDS


def get_callbacks(app):
    @app.callback(
        Output("posts_per_hour_graph", "figure"),
        Output("sentiment_graph", "figure"),
        Input("posts_per_hour_checklist", "value"),
        Input("update-interval", "n_intervals"),
    )
    def update_charts(teams, _):
        global HOURLY_POSTS_DF, AVERAGE_SENTIMENT_DF, DAILY_DATA_DF, PICKED_TEAMS
        PICKED_TEAMS = teams
        triggered = ctx.triggered_id
        if triggered == "update-interval":
            WORDCLOUDS = {}
            try:
                today = datetime.today().date()
                df = get_data(today)
            except Exception as e:
                df = get_data(today - timedelta(days=1))

            DAILY_DATA_DF = preprocess_main_dataframe(df)

            # AGGREGATIONS FROM DAILY_DATA_DF
            HOURLY_POSTS_DF = (
                DAILY_DATA_DF.groupby(["bracket_timestamp", "team"])
                .score.count()
                .reset_index()
            )

            AVERAGE_SENTIMENT_DF = (
                DAILY_DATA_DF.groupby(["bracket_timestamp", "team"])
                .compound_sentiment.mean()
                .reset_index()
            )
            print("Updated data sources!")

        fig_hour = update_line_chart(HOURLY_POSTS_DF, teams)
        fig_sentiment = update_bar_chart(AVERAGE_SENTIMENT_DF, teams)
        return fig_hour, fig_sentiment

    @app.callback(
        Output("image_wc", "src"),
        Output("tsne", "figure"),
        Input("wordcloud_team_selection", "value"),
    )
    def make_wordcloud(team):
        if WORDCLOUDS.get(team, False):
            return WORDCLOUDS[team]

        data = DAILY_DATA_DF[DAILY_DATA_DF.team == team]
        processed_texts = preprocess_texts(data["body"])
        sentences = sent_to_words(processed_texts)
        tokens = [
            [word for word in doc if word not in STOPWORDS and len(word) > 1]
            for doc in sentences
        ]

        all_words = []
        for token in tokens:
            all_words += token

        img = BytesIO()
        plot_wordcloud(corpus=all_words).save(img, format="PNG")

        # vis_path = generate_lda_vis(tokens, team)
        fig = generate_tsne(tokens, data["body"], team)

        final_image = "data:image/png;base64,{}".format(
            base64.b64encode(img.getvalue()).decode()
        )

        WORDCLOUDS[team] = (
            final_image,
            fig,
        )

        return WORDCLOUDS[team]

    @app.callback(
        Output("search-bar-div", "children"),
        Output("left-graph", "children"),
        Output("right-graph", "children"),
        Input("tabs-picker", "value"),
    )
    def render_content(active):
        if active == "nba":
            team_multiselect = dmc.MultiSelect(
                label="Select team(s)",
                placeholder="Select your preferred NBA team(s)",
                id="posts_per_hour_checklist",
                value=["Los Angeles Lakers", "Golden State Warriors"],
                data=NBA_TEAMS,
                clearable=True,
                searchable=True,
                nothingFound="Not found",
            )
            posts_per_hour_graph = dcc.Graph(id="posts_per_hour_graph")
            sentiment_graph = dcc.Graph(id="sentiment_graph")
            return team_multiselect, posts_per_hour_graph, sentiment_graph
        else:
            team_select = (
                dmc.Select(
                    label="Select a team",
                    placeholder="Select your preferred NBA team(s)",
                    id="wordcloud_team_selection",
                    value="Memphis Grizzlies",
                    data=NBA_TEAMS,
                    clearable=True,
                    searchable=True,
                    nothingFound="Not found",
                    className="search-bar",
                ),
            )
            wc_image = html.Div(
                [
                    html.H5("Most common words posted in the subreddit"),
                    html.Img(id="image_wc"),
                ],
                className="team-wide-graph",
            )
            test = dcc.Graph(id="tsne")

            return team_select, wc_image, test
