from dash import html, dcc
import dash_mantine_components as dmc

from config import *
from helpers import *
from data import *


def create_layout():
    title_component = html.H1(
        "Trendba",
        className="title",
        style={
            "text-align": "center",
            "margin": "5% 0 2.5% 0",
            "display": "inline-block",
        },
    )
    return html.Div(
        [
            # Header Div
            html.Div(
                [
                    html.Div(
                        [
                            dmc.Tooltip(
                                label="ℹ️ Pronounced as Trend-B-A (Spell out NBA but replace the N with Trend)",
                                position="top",
                                offset=0,
                                children=title_component,
                                withArrow=True,
                            )
                        ],
                        style={
                            "justify-content": "center",
                            "margin": "2.5% 0 2.5% 0",
                            "display": "flex",
                        },
                    ),
                    html.P(
                        "An Analytics Dashboard for NBA Subreddits - Updated Hourly! ⌛️",
                        style={
                            "text-align": "center",
                            "margin": "-2% 0 2.5% 0",
                        },
                    ),
                ],
                className="header",
            ),
            dmc.Divider(variant="solid"),
            # Search Bar Div
            html.Div(
                [
                    dmc.MultiSelect(
                        label="Select team(s)",
                        placeholder="Select your preferred NBA team(s)",
                        id="posts_per_hour_checklist",
                        value=["Los Angeles Lakers", "Golden State Warriors"],
                        data=NBA_TEAMS,
                        clearable=True,
                        searchable=True,
                        nothingFound="Not found",
                    )
                ],
                style=dict(
                    width="50%", display="inline-block", padding="2.5% 2.5% 0 2.5%"
                ),
            ),
            # NBA-Wide Visualizations
            html.Div(
                [
                    dcc.Graph(
                        id="posts_per_hour_graph",
                    ),
                    dcc.Graph(id="sentiment_graph"),
                ],
                # top right bottom left
                style={
                    "display": "flex",
                    "align-items": "flex-start",
                    "flex-wrap": "wrap",
                },
            ),
        ]
    )
