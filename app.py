import math
from fractions import Fraction
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from constants import *

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(
    children=[
        html.H1(children="Decision Support Tool", style={"textAlign": "center"}),
        html.Div(
            children="Decision Support Tool for Mr. Jaeger in the Freemark Abbey Winery case.",
            style={"textAlign": "center"},
        ),
        html.H3(children="Probability of storm"),
        dcc.Slider(
            id="input_p_storm",
            min=0,
            max=1,
            step=1 / 15,
            marks={
                i / 15: "{}".format(str(Fraction(i / 15).limit_denominator()))
                for i in range(0, 16)
            },
            value=2 / 3,
        ),
        html.H3(children="Probability of mold forming if there is a storm"),
        dcc.Slider(
            id="input_p_mold",
            min=0,
            max=1,
            step=1 / 15,
            marks={
                i / 15: "{}".format(str(Fraction(i / 15).limit_denominator()))
                for i in range(0, 16)
            },
            value=0.4,
        ),
        html.H3(children="Probability of acidity dropping below 20%"),
        dcc.Slider(
            id="input_p_lo_acidity",
            min=0,
            max=1,
            step=1 / 15,
            marks={
                i / 15: "{}".format(str(Fraction(i / 15).limit_denominator()))
                for i in range(0, 16)
            },
            value=0.2,
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H3(children="Certain Equivalent for harvest ($)"),
                        html.Div(id="out-x-harvest", style={"textAlign": "center"}),
                    ]
                ),
                html.Div(
                    [
                        html.H3(children="Certain Equivalent for wait ($)"),
                        html.Div(id="out-x-wait", style={"textAlign": "center"}),
                    ]
                ),
            ],
            style={"display": "flex", "justifyContent": "space-around"},
        ),
        html.Div([html.H2(children="Final Recommendation"), html.Div(id="out-rec")], style={"textAlign": "center"}),
        html.Div([html.H3(children="Value of spores"), html.Div(id="out-v-spores")], style={"textAlign": "center"}),
        html.Div([html.H3(children="Recommendation on spores"), html.Div(id="out-rec-spores")], style={"textAlign": "center"}),
    ],
    style={"fontSize": "24px"},
)


def get_u(x):
    return -math.exp(-x / rho)


def get_x(u):
    return -rho * math.log(-u)


rho = 72000
u_harvest = get_u(x_harvest)
u_wait_storm_mold = get_u(x_wait_storm_mold)
u_wait_storm_no_mold = get_u(x_wait_storm_no_mold)
u_wait_no_storm_lo_acidity = get_u(x_wait_no_storm_lo_acidity)
u_wait_no_storm_hi_sugar = get_u(x_wait_no_storm_hi_sugar)
u_wait_no_storm_lo_sugar = get_u(x_wait_no_storm_lo_sugar)
u_wait_no_storm_nor_acidity = (
    0.5 * u_wait_no_storm_hi_sugar + 0.5 * u_wait_no_storm_lo_sugar
)  # expose this?

p_storm = 2 / 3
p_mold = 0.4
p_lo_acidity = 0.2


@app.callback(
    [
        Output(component_id="out-x-harvest", component_property="children"),
        Output(component_id="out-x-wait", component_property="children"),
        Output(component_id="out-rec", component_property="children"),
        Output(component_id="out-v-spores", component_property="children"),
        Output(component_id="out-rec-spores", component_property="children"),
    ],
    [
        Input(component_id="input_p_storm", component_property="value"),
        Input(component_id="input_p_mold", component_property="value"),
        Input(component_id="input_p_lo_acidity", component_property="value"),
    ],
)
def update(p_storm, p_mold, p_lo_acidity):
    u_wait_storm = p_mold * u_wait_storm_mold + (1 - p_mold) * u_wait_storm_no_mold
    u_wait_no_storm = (
        p_lo_acidity * u_wait_no_storm_lo_acidity
        + (1 - p_lo_acidity) * u_wait_no_storm_nor_acidity
    )
    u_wait = p_storm * u_wait_storm + (1 - p_storm) * u_wait_no_storm
    x_wait = round(get_x(u_wait))
    if x_harvest >= x_wait:
        rec = "Mr. Jaeger should harvest."
    else:
        rec = "Mr. Jaeger should wait."
    # spores
    u_spores = p_storm * u_wait_storm_mold + (1 - p_storm) * u_wait_no_storm
    x_spores = round(get_x(u_spores))
    v_spores = x_spores - max(x_harvest, x_wait)
    rec_spores = "Mr. Jaeger should not buy the spores."
    if v_spores > 10000:
        rec_spores = "Mr. Jaeger should buy the spores."
    return x_harvest, x_wait, rec, v_spores, rec_spores


if __name__ == "__main__":
    app.run_server(debug=True)
