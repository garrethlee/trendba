from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from config import *
from helpers import *
from data import *


def create_layout():
    update_data_and_plots()
    title_component = html.H1(
        f"🏀 Trendba 🏀",
        className="title",
    )
    return html.Div(
        [
            # Update every 10 minutes
            dcc.Interval(id="update-interval", interval=1000 * 60 * 20),
            # Header Div
            html.Div(
                [
                    html.Div(
                        [
                            dmc.Tooltip(
                                label="ℹ️ Pronounced Trend-B-A (Spell out NBA but replace the N with Trend)",
                                position="top",
                                offset=0,
                                children=title_component,
                                withArrow=True,
                            )
                        ],
                        # top right bottom left
                        style={
                            "justify-content": "center",
                            "padding": "2.5% 0 0 0",
                            "display": "flex",
                        },
                    ),
                    html.P(
                        "An Analytics Dashboard for NBA Subreddits - Updated Hourly! ⌛️",
                        className="subtitle",
                    ),
                    html.P(
                        f"Last updated: {datetime.today().minute} minutes ago",
                        className="subtitle",
                    ),
                ],
                className="header",
            ),
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab("NBA", value="nba"),
                            dmc.Tab("Team", value="team"),
                        ]
                    ),
                ],
                id="tabs-picker",
                value="nba",
                className="tabs",
            ),
            # Search Bar Div
            html.Div(
                id="search-bar-div",
                className="search-bar",
            ),
            # NBA-Wide Visualizations
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    id="left-graph",
                                ),
                                width=6,
                                className="nba-wide-graph",
                            ),
                            dbc.Col(
                                html.Div(
                                    id="right-graph",
                                ),
                                width=6,
                                className="nba-wide-graph",
                                style={"height": "100%"},
                            ),
                        ]
                    )
                ],
                className="nba-wide-div",
            ),
        ]
    )
