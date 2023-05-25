from dash import Dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

from helpers import *
from config import *
from callbacks import *
from layouts import *


# CERULEAN, COSMO, CYBORG, DARKLY, FLATLY,
# JOURNAL, LITERA, LUMEN, LUX, MATERIA,
# MINTY, MORPH, PULSE, QUARTZ, SANDSTONE,
# SIMPLEX, SKETCHY, SLATE, SOLAR, SPACELAB,
# SUPERHERO, UNITED, VAPOR, YETI, ZEPHYR
app = Dash(
    __name__, external_stylesheets=[dbc.themes.MINTY], suppress_callback_exceptions=True
)

load_figure_template("COSMO")

if __name__ == "__main__":
    app.layout = create_layout
    get_callbacks(app)
    app.run_server(host="0.0.0.0", port=8050)
