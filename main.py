import dash_bootstrap_components as dbc
import dash
from dash import html, dcc, Input, Output, State, dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from statistics import stdev
from copy import copy, deepcopy
from random import random

from functions import *

import_df = pd.read_csv("set2.csv")
df = copy(import_df)

full_edit_counter = 0
selection_edit_counter = 0
town_edit_counter = 0

last_full_edit_counter = 0
last_reset_button_counter = 0

# Create the app and set the theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    # dbc.Row([
    #     dbc.Col(html.H1('Dashboard'), width=12),
    # ]),

    dbc.Row([
        dbc.Col([
            html.Div(children=[
                html.Div("Template Type", style={'display': 'inline-block', "width": "10%"}),
                dcc.Dropdown(options=["All"] + template_types, value="All", id="template_dropdown",
                             style={'display': 'inline-block', "width": "35%"}),
                html.Div("Color", style={'display': 'inline-block', "width": "10%"}),
                dcc.Dropdown(options=["any", "non-white", "red", "blue", "white"], value="any", id="color_dropdown",
                             style={'display': 'inline-block', "width": "35%"}),
                html.Div(id="town_selection"),
                html.Div(id="jitter_selection"),
            ]),
        ]),
    ]),

    dcc.Tabs(id='tabs', children=[
        dcc.Tab(label='Model', children=[
            # Contents of Tab 1
        ]),

        dcc.Tab(label='Heatmap', children=[
            dbc.Row([
                dbc.Col(html.H3('Matchup Spread'), width=12),
                html.Div([
                    html.Button("Reset Selection", id="reset_selection_button", style={"display": "inline-block"}),
                    html.Div("Matchups are only shown if at least 8 games were played", style={"display": "inline-block"}),
                ]),
                dbc.Col([
                    dcc.Graph(id="town_V_town_graph", config={'displayModeBar': False}),
                    dcc.Checklist(options=["bidding", "win rate", "bidding variance"], value=["bidding"], id="town_V_town_check"),
                    dcc.Store(data=[], id="town_V_town_state"),
                ]),
            ]),
        ]),

        dcc.Tab(label='Graphs', children=[
            dbc.Row([
                dbc.Col(html.H3('Matchup Analysis'), width=12),
                # dbc.Col([
                #     html.Div(children=[
                #         html.Div("Player 1", style={'display': 'inline-block', "width": "5%"}),
                #         dcc.Dropdown(towns, value=towns[0], id='town_A_town_dropdown_1', style={'display': 'inline-block', "width": "35%"}),
                #         html.Div("Player 2", style={'display': 'inline-block', "width": "5%"}),
                #         dcc.Dropdown(["all"] + towns, value="all", id='town_A_town_dropdown_2', style={'display': 'inline-block', "width": "35%"})
                #     ]),
                # ]),
                html.Div(children=[
                    html.Div(id='town_A_town_prediction', style={'display': 'inline-block', "width": "19%", "height": "25%", 'font-size': '26px', "align": "center", 'align-items': 'center', 'justify-content': 'center'}),
                    html.Div(dcc.Graph(id="town_A_town_boxplot", config={'displayModeBar': False}), style={'display': 'inline-block', "width": "19%", "height": "25%"}),
                    html.Div(dcc.Graph(id="town_A_town_jitter", config={'displayModeBar': False}), style={'display': 'inline-block', "width": "39%", "height": "25%"}),
                ]),
                dbc.Col([
                    dcc.Graph(id="town_A_town_bar", config={'displayModeBar': False}),
                    dcc.Checklist(options=["bidding", "turns"], value=["bidding"], id="town_A_town_bar_check"),
                    dcc.Store(data=[], id="town_A_town_bar_check_state"),
                    html.Div(children=[
                        html.Div("Number of Quantiles", style={"display": "inline-block", "width": "14%"}),
                        html.Div(dcc.Slider(min=1, max=10, step=1, value=5, id='town_A_town_bar_slider'), style={"display": "inline-block", "width": "84%"}),
                    ]),
                ]),
            ]),
        ]),

        dcc.Tab(label='Table', children=[
            dbc.Col([
                html.Label("Hero Stats"),
                dash_table.DataTable(sort_action='native', id="town_A_town_heroes")
            ]),
        ]),
    ]),
    dcc.Store(data=[0], id="dataset_full"),
    dcc.Store(data=[0], id="dataset_selection"),
    dcc.Store(data=[0], id="town_V_town_update"),
    dcc.Store(data=[], id="selection"),
    dcc.Store(id="dummy"),
])



# Define the callback for updating the dropdown menus based on the selected template
@app.callback(
    Output('dataset_full', 'data'),
    Input('template_dropdown', 'value'),
    Input('color_dropdown', 'value'),
)
def update_df(template, color):
    # Filter data based on the selected template
    global df, full_edit_counter

    if template == "All":
        df = copy(import_df)
    else:
        df = import_df[import_df['template_type'] == template]
    
    if color == "non-white":
        df = df[df["color"] != "white"]
    elif color != "any":
        df = df[df["color"] == color]

    full_edit_counter += 1

    return [full_edit_counter]


@app.callback(
    Output("town_selection", "children"),
    Output("selection", "data"),
    Input('town_V_town_graph', 'clickData'),
    Input("selection", "data"),
    Input("reset_selection_button", "n_clicks"),
    Input("dataset_full", "data")
    )
def update_selection(click_data, selection, reset_button, dummy):
    global last_reset_button_counter

    if reset_button != last_reset_button_counter:
        selection = []
        last_reset_button_counter = reset_button

    elif click_data != None:
        selected = [click_data["points"][0]["y"], click_data["points"][0]["x"]]

        if selected in selection:
            selection.remove(selected)
        else:
            selection.append(selected)
    
    return str(selection), selection

@app.callback(
    Output("dataset_selection", "data"),
    Input("selection", "data"),
    Input("dataset_full", "data"),
)
def update_selection_df(selection, dummy):
    global fig_winrate, fig_bidding, fig_bidding_variance
    global selection_df, selection_edit_counter, last_full_edit_counter

    if selection != []:
        selection_df = pd.concat([df[(df["town"] == i[0]) & (df["opponent_town"] == i[1])] for i in selection])
    else:
        selection_df = copy(df)

    if last_full_edit_counter != dummy:
        fig_winrate, fig_bidding, fig_bidding_variance = create_town_v_town_graphs(df, selection)

    else:
        for fig in [fig_winrate, fig_bidding, fig_bidding_variance]:
            text = deepcopy(fig.data[0]["z"])

            for highlight in selection:
                text[towns[::-1].index(highlight[0])][towns[::-1].index(highlight[1])] = f"> {text[towns[::-1].index(highlight[0])][towns[::-1].index(highlight[1])]} <"
            
            fig.data[0]["text"] = text


    last_full_edit_counter = dummy
    selection_edit_counter += 1

    return [selection_edit_counter]


@app.callback(
    Output("town_V_town_graph", "figure"),
    Output("town_V_town_check", "value"),
    Output("town_V_town_state", "data"),
    Input("town_V_town_check", "value"),
    Input("town_V_town_state", "data"),
    Input("dataset_selection", "data"))
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
    Input("dataset_selection", "data"))
def town_A_town(dummy):
    sub_df = selection_df

    boxplot = bidding_boxplot(sub_df)
    jitter = town_A_town_jitter(sub_df)
    heroes_data, heroes_columns = heroes_table(sub_df)

    prediction = get_optimal_player_1_bid(sub_df)
    prediction_text = f"Our model indicates the optimal bid for player 1 would be around {prediction}"

    return boxplot, jitter, prediction_text, heroes_data, heroes_columns 


@app.callback(
    Output("jitter_selection", "children"),
    Input("town_A_town_jitter", "relayoutData"),
)
def get_jitter_selection(limits):
    return str(limits)


@app.callback(
    Output("town_A_town_bar", "figure"),
    Output("town_A_town_bar_check", "value"),
    Output("town_A_town_bar_check_state", "data"),
    Input("town_A_town_bar_check", "value"),
    Input("town_A_town_bar_check_state", "data"),
    Input("town_A_town_bar_slider", "value"),
    Input("dataset_selection", "data"))
def town_graph(value, state, quantiles, dummy):
    sub_df = selection_df

    value = list(set(value) - set(state))

    graph_value = state if value == [] else value
    graph = variable_result_graph(sub_df, graph_value[0], quantiles)
    return graph, graph_value, graph_value

if __name__ == '__main__':
    app.run_server(debug=True)