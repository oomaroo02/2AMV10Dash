import dash_bootstrap_components as dbc
import dash
from dash import html, dcc, Input, Output, dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from statistics import stdev
from copy import copy
from random import random

from functions import *

import_df = pd.read_csv("set2.csv")
df = copy(import_df)
template_edit_counter = 0

# Create the app and set the theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = html.Div([
    dbc.Row([
        dbc.Col(html.H1('Dashboard'), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Dropdown(options = ["All"]+template_types, value="All", id="template_dropdown"), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.H3('Section 1'), width=12),
        dbc.Col(
            [dcc.Graph(config={'displayModeBar': False}, id="town_V_town_graph"),
             dcc.Checklist(options=["bidding", "win rate", "bidding variance"], value=["bidding"],
                           id="town_V_town_check"),
             dcc.Store(data=[], id="town_V_town_state")
        ])
    ]),
    dbc.Row([
        dbc.Col(html.H3('Section 2'), width=12),
        dbc.Col([
            dash_table.DataTable(sort_action='native', id="town_A_town_heroes"),
            dcc.Graph(id="town_A_town_boxplot"),
            dcc.Graph(id="town_A_town_jitter", config={'displayModeBar': False}),
            dcc.Graph(id="town_A_town_bar"),
            dcc.Checklist(options=["bidding", "turns"], value=["bidding"], id="town_A_town_bar_check"),
            dcc.Store(data=[], id="town_A_town_bar_check_state"),
            dcc.Slider(min=1, max=10, step=1, value=5, id='town_A_town_bar_slider'),
            dcc.Dropdown(towns, value=towns[0], id='town_A_town_dropdown_1'),
            dcc.Dropdown(["all"] + towns, value="all", id='town_A_town_dropdown_2')]),
    ]),

    dcc.Store(data = [0], id="dataset")
])


# Define the callback for updating the dropdown menus based on the selected template
@app.callback(
    [Output('dataset', 'data')],
    [Input('template_dropdown', 'value')]
)
def update_dropdowns(template):
    # Filter data based on the selected template
    global df, fig_winrate, fig_bidding, fig_bidding_variance, template_edit_counter

    if template == "All":
        df = copy(import_df)
    else:
        df = import_df[import_df['template_type'] == template]

    fig_winrate, fig_bidding, fig_bidding_variance = create_town_v_town_graphs(df)

    template_edit_counter += 1

    return [template_edit_counter]


@app.callback(
    Output("town_V_town_graph", "figure"),
    Output("town_V_town_check", "value"),
    Output("town_V_town_state", "data"),
    Input("town_V_town_check", "value"),
    Input("town_V_town_state", "data"),
    Input("dataset", "data"))
def update_section1(value, state, dummy):
    value = list(set(value) - set(state))

    if value == ["bidding"] or (value == [] and state == ["bidding"]):
        return fig_bidding, ["bidding"], ["bidding"]

    elif value == ["win rate"] or (value == [] and state == ["win rate"]):
        return fig_winrate, ["win rate"], ["win rate"]

    elif value == ["bidding variance"] or (value == [] and state == ["bidding variance"]):
        return fig_bidding_variance, ["bidding variance"], ["bidding variance"]


@app.callback(
    Output("town_A_town_boxplot", "figure"),
    Output("town_A_town_jitter", "figure"),
    Output("town_A_town_heroes", "data"),
    Output("town_A_town_heroes", "columns"),
    Input("town_A_town_dropdown_1", "value"),
    Input("town_A_town_dropdown_2", "value"),
    Input("dataset", "data"))
def town_A_town(town1, town2, dummy):
    sub_df = df[df["town"] == town1] if town2 == "all" else df[
        (df["town"] == town1) & (df["opponent_town"] == town2)]

    boxplot = bidding_boxplot(sub_df)
    jitter = town_A_town_jitter(sub_df)
    heroes_data, heroes_columns = heroes_table(sub_df)

    return boxplot, jitter, heroes_data, heroes_columns


@app.callback(
    Output("town_A_town_bar", "figure"),
    Output("town_A_town_bar_check", "value"),
    Output("town_A_town_bar_check_state", "data"),
    Input("town_A_town_bar_check", "value"),
    Input("town_A_town_bar_check_state", "data"),
    Input("town_A_town_bar_slider", "value"),
    Input("town_A_town_dropdown_1", "value"),
    Input("town_A_town_dropdown_2", "value"),
    Input("dataset", "data"))
def town_graph(value, state, quantiles, town1, town2, dummy):
    sub_df = df[df["town"] == town1] if town2 == "all" else df[
        (df["town"] == town1) & (df["opponent_town"] == town2)]

    value = list(set(value) - set(state))

    graph_value = state if value == [] else value
    graph = variable_result_graph(sub_df, graph_value[0], quantiles)
    return graph, graph_value, graph_value

if __name__ == '__main__':
    app.run_server(debug=True)
