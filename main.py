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
        dbc.Col(html.H1('Dashboard'), width=12),
    ]),

    dbc.Row([
        dbc.Col([
            html.Div(children=[
                html.Div("Template Type", style={'display': 'inline-block', "width":"10%"}),
                dcc.Dropdown(options = ["All"]+template_types, value="All", id="template_dropdown", style={'display': 'inline-block', "width":"35%"}),
            ]),
        ]),
    ]),

    dbc.Row([
        dbc.Col(html.H3('Matchup Spread'), width=12),
        dbc.Col(
            [dcc.Graph(id="town_V_town_graph", config={'displayModeBar': False}),
             dcc.Checklist(options=["bidding", "win rate", "bidding variance"], value=["bidding"],
                           id="town_V_town_check"),
             dcc.Store(data=[], id="town_V_town_state"),
        ]),
    ]),

    dbc.Row([
        dbc.Col(html.H3('Matchup Analysis'), width=12),
        dbc.Col([
            html.Div(children=[
                html.Div("Player 1", style={'display': 'inline-block', "width":"5%"}),
                dcc.Dropdown(towns, value=towns[0], id='town_A_town_dropdown_1', style={'display': 'inline-block', "width":"35%"}),
                html.Div("Player 2", style={'display': 'inline-block', "width":"5%"}),
                dcc.Dropdown(["all"] + towns, value="all", id='town_A_town_dropdown_2', style={'display': 'inline-block',"width":"35%"})]),
            html.Div([html.Label("Hero Stats"),
                      dash_table.DataTable(sort_action='native', id="town_A_town_heroes")
            ]),
            
            html.Div([
                html.Div(id="town_A_town_prediction", style={'display': 'inline-block', "width":"20%", "height": "25%"}),
                html.Div(dcc.Graph(id="town_A_town_boxplot", config={'displayModeBar': False}), style={'display': 'inline-block', "width":"40%", "height": "25%"}),
                html.Div(dcc.Graph(id="town_A_town_jitter", config={'displayModeBar': False}), style={'display': 'inline-block', "width":"40%", "height": "25%"}),  
            ]),
            
            dcc.Graph(id="town_A_town_bar", config={'displayModeBar': False}),
            dcc.Checklist(options=["bidding", "turns"], value=["bidding"], id="town_A_town_bar_check"),
            dcc.Store(data=[], id="town_A_town_bar_check_state"),
            dcc.Slider(min=1, max=10, step=1, value=5, id='town_A_town_bar_slider'),
        ]),
    ]),

    dcc.Store(data = [0], id="dataset"),
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
    Output("town_A_town_prediction", "children"),
    Output("town_A_town_heroes", "data"),
    Output("town_A_town_heroes", "columns"),
    Input("town_A_town_dropdown_1", "value"),
    Input("town_A_town_dropdown_2", "value"),
    Input("dataset", "data"))
def town_A_town(town1, town2, dummy):
    sub_df = copy(df[df["town"] == town1]) if town2 == "all" else copy(df[
        (df["town"] == town1) & (df["opponent_town"] == town2)])

    boxplot = bidding_boxplot(sub_df)
    jitter = town_A_town_jitter(sub_df)
    heroes_data, heroes_columns = heroes_table(sub_df)

    prediction = get_optimal_player_1_bid(sub_df)
    prediction_text = f"Our model indicates the optimal bid for the {town1} player would be around {prediction}"

    return boxplot, jitter, prediction_text, heroes_data, heroes_columns


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
    sub_df = copy(df[df["town"] == town1]) if town2 == "all" else copy(df[
        (df["town"] == town1) & (df["opponent_town"] == town2)])

    value = list(set(value) - set(state))

    graph_value = state if value == [] else value
    graph = variable_result_graph(sub_df, graph_value[0], quantiles)
    return graph, graph_value, graph_value

if __name__ == '__main__':
    app.run_server(debug=True)
