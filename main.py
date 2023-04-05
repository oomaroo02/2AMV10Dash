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

# These counters are used to keep track when selections on the graph change
full_edit_counter = 0
selection_edit_counter = 0
limit_edit_counter = 0

last_full_edit_counter = 0
last_reset_button_counter = 0

# Create the app and set the theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    # dbc.Row([
    #     dbc.Col(html.H1('Dashboard'), width=12),
    # ]),
    
    # The upper filter bar
    html.Div(children=[
        html.Div("Template Type", style={'display': 'inline-block', "width": "10%"}),
        dcc.Dropdown(options=["All"] + template_types, value="All", id="template_dropdown",
                     style={'display': 'inline-block', "width": "30%"}),
        html.Div("Color", style={'display': 'inline-block', "width": "10%"}),
        dcc.Dropdown(options=["any", "non-white", "red", "blue", "white"], value="any", id="color_dropdown",
                     style={'display': 'inline-block', "width": "30%"}),
    ]),

    # Used for debugging
    # html.Div(id="town_selection"),
    # html.Div(id="jitter_selection"),

    # The four tabs
    dcc.Tabs(id='tabs', children=[
    
        # Tab with the model
        dcc.Tab(label='Model', children=[
            html.Div(dcc.Dropdown(towns, placeholder="town (player 1)", id='model_town_1'), style={"width": "30%"}),
            html.Div(dcc.Dropdown([], placeholder="hero (player 1)", id='model_hero_1'), style={"width": "30%"}),
            dcc.Input(type="number", placeholder="bidding (player 1's perspective)", id="model_bidding", style={"width": "30%"}),
            html.Div(dcc.Dropdown(towns, placeholder="town (player 2)", id='model_town_2'), style={"width": "30%"}),
            html.Div(dcc.Dropdown([], placeholder="hero (player 2)", id='model_hero_2'), style={"width": "30%"}),
            html.Div(id='model_result'),
        ]),

        # Tab with the town versus town matchup heatmap
        dcc.Tab(label='Heatmap', children=[
            dbc.Col(html.H3('Matchup Spread'), width=12),

            html.Div("Matchups are only shown if at least 8 games were played"),
            html.Button("Reset Selection", id="reset_selection_button"),

            dbc.Col([
                dcc.Graph(id="town_V_town_graph", config={'displayModeBar': False}),
                dcc.Checklist(options=["bidding", "win rate", "bidding variance"], value=["bidding"], id="town_V_town_check"),
                dcc.Store(data=[], id="town_V_town_state"),
            ]),
        ]),

        # Tab with the different 'bidding' graphs
        dcc.Tab(label='Graphs', children=[
            html.Div(children=[ 
                dcc.Graph(id="town_A_town_jitter", config={'displayModeBar': False}, style={'display': 'inline-block', "width": "39%", "height": "35vh"}),
                dcc.Graph(id="town_A_town_boxplot", config={'displayModeBar': False}, style={'display': 'inline-block', "width": "19%", "height": "35vh"}),
                html.Span(id='town_A_town_prediction', style={'display': 'inline-block', "width": "19%",'fontSize': '16px', "height": "1vh"}),
            ]),
            
            html.Div(children=[
                dcc.Graph(id="town_A_town_bar", config={'displayModeBar': False}, style={"height": "40vh"}),
                dcc.Checklist(options=["bidding", "turns"], value=["bidding"], id="town_A_town_bar_check"),
                dcc.Store(data=[], id="town_A_town_bar_check_state"),
                html.Div(children=[
                    html.Div("Number of Quantiles", style={"display": "inline-block", "width": "14%"}),
                    html.Div(dcc.Slider(min=1, max=10, step=1, value=5, id='town_A_town_bar_slider'), style={"display": "inline-block", "width": "84%"}),
                ]),
            ]),
        ]),

        # Tab with the hero table
        dcc.Tab(label='Table', children=[
            dbc.Col([
                html.Label("Hero Stats"),
                dash_table.DataTable(sort_action='native', id="town_A_town_heroes")
            ]),
        ]),
    ]),

    dcc.Store(data=[0], id="dataset_full"), # Keeps track when the filtering changes
    dcc.Store(data=[0], id="dataset_selection"), # Keeps track when the selection on the heatmap changes
    dcc.Store(data=[0], id="dataset_limit"), # Keeps track of when the bidding limits on the jitter graph change
    dcc.Store(data=[], id="selection"), # Keeps track of teh selection on the heatmap
    dcc.Store(id="dummy"), # Used for debugging
])



# For the model dropdown where the heros are chosen, make the dropdowns show the heros for the currently selected town
@app.callback(
    Output("model_hero_1", "options"),
    Output("model_hero_1", "placeholder"),
    Input("model_town_1", "value"),
)
def update_hero1_dropdown(town):
    if town in towns:
        return heroes_per_town[town], f"{town} hero (player 1)"
    return [], "hero (player 1)"


@app.callback(
    Output("model_hero_2", "options"),
    Output("model_hero_2", "placeholder"),
    Input("model_town_2", "value"),
)
def update_hero2_dropdown(town):
    if town in towns:
        return heroes_per_town[town], f"{town} hero (player 2)"
    return [], "hero (player 2)"


# Runs the model
@app.callback(
    Output("model_result", "children"),
    Input("model_town_1", "value"),
    Input("model_town_2", "value"),
    Input("model_bidding", "value"),
    Input("model_hero_1", "value"),
    Input("model_hero_2", "value"),
)
def update_model(town1, town2, bidding, hero1, hero2):
    if (town1 not in towns):
        return "No town for player 1"
    
    elif (town2 not in towns):
        return "No town for player 2"
    
    elif (not bidding):
        return "No bidding added"
    
    elif (hero1 not in heroes_per_town[town1]):
        return "No hero for player 1"
    
    elif (hero2 not in heroes_per_town[town2]):
        return "No hero for player 2"
    
    result = run_model(town1, town2, int(bidding))

    return f"Expected winrate is {result}"
    
    
# Filter data based on the selected template and selected color
@app.callback(
    Output('dataset_full', 'data'),
    Input('template_dropdown', 'value'),
    Input('color_dropdown', 'value'),
)
def update_df(template, color):
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


# Updates the 'selection' data whenever matchups in the heatmap are selected
@app.callback(
    Output("selection", "data"),
    # Output("town_selection", "children"),
    Input('town_V_town_graph', 'clickData'),
    Input("selection", "data"),
    Input("reset_selection_button", "n_clicks"),
    Input("dataset_full", "data")
    )
def update_selection(click_data, selection, reset_button, dummy):
    global last_reset_button_counter

    if reset_button != last_reset_button_counter: # If the reset button was pressed
        selection = []
        last_reset_button_counter = reset_button

    elif click_data != None: # If something was clicked
        selected = [click_data["points"][0]["y"], click_data["points"][0]["x"]]

        # If already selected deselect, otherwise select matchup
        if selected in selection:
            selection.remove(selected)
        else:
            selection.append(selected)
    
    return selection #, str(selection)


# Updates the selection data whenever either the full data or the selection changes
# Also updates the heatmap
@app.callback(
    Output("dataset_selection", "data"),
    Input("selection", "data"),
    Input("dataset_full", "data"),
)
def update_selection_df(selection, dummy):
    global fig_winrate, fig_bidding, fig_bidding_variance
    global selection_df, selection_edit_counter, last_full_edit_counter


    if selection != []: # If there are mathcups selected
        selection_df = pd.concat([df[(df["town"] == i[0]) & (df["opponent_town"] == i[1])] for i in selection])
    else:
        selection_df = copy(df)

    if last_full_edit_counter != dummy: # If the filtering was changed
        fig_winrate, fig_bidding, fig_bidding_variance = create_town_v_town_graphs(df, selection)

    else: # update the visual selection without rerunning graph creation
        for fig in [fig_winrate, fig_bidding, fig_bidding_variance]:
            text = deepcopy(fig.data[0]["z"])

            for highlight in selection:
                text[towns[::-1].index(highlight[0])][towns[::-1].index(highlight[1])] = f"> {text[towns[::-1].index(highlight[0])][towns[::-1].index(highlight[1])]} <"
            
            fig.data[0]["text"] = text

    last_full_edit_counter = dummy
    selection_edit_counter += 1

    return [selection_edit_counter]


# Allows for switching between the different heatmaps
@app.callback(
    Output("town_V_town_graph", "figure"),
    Output("town_V_town_check", "value"),
    Output("town_V_town_state", "data"),
    Input("town_V_town_check", "value"),
    Input("town_V_town_state", "data"),
    Input("dataset_selection", "data"))
def update_heatmap(value, state, dummy):
    value = list(set(value) - set(state)) # Turns value into the checkbox that was just checked

    if value == ["bidding"] or (value == [] and state == ["bidding"]):
        return fig_bidding, ["bidding"], ["bidding"]

    elif value == ["win rate"] or (value == [] and state == ["win rate"]):
        return fig_winrate, ["win rate"], ["win rate"]

    elif value == ["bidding variance"] or (value == [] and state == ["bidding variance"]):
        return fig_bidding_variance, ["bidding variance"], ["bidding variance"]


# Creates the jitter graph and updates it when the data changes
@app.callback(
    Output("town_A_town_jitter", "figure"),
    Input("dataset_selection", "data"))
def update_jitter_graph(dummy):
    sub_df = selection_df

    jitter = town_A_town_jitter(sub_df)

    return jitter


# Changes the data used for the non-heatmap/jitter graph when the jitter graph is zoomed
# KNOWN BUG: relayoutData resets whenever you change to a different tab and back
@app.callback(
    Output("dataset_limit", "data"),
    Input("town_A_town_jitter", "relayoutData"),
    Input("dataset_selection", "data"),
)
def get_jitter_selection(limits, dummy):
    global limit_df, limit_edit_counter

    if limits == None or not (('yaxis.range[0]' in limits) and ('yaxis.range[1]' in limits)):
        limit_df = copy(selection_df)
    else:
        limit_df = selection_df[(selection_df["bidding"] >= limits['yaxis.range[0]']) & (selection_df["bidding"] <= limits['yaxis.range[1]'])]

    limit_edit_counter += 1

    return limit_edit_counter


# Handles the boxplot, prediction text and hero table
@app.callback(
    Output("town_A_town_boxplot", "figure"),
    Output("town_A_town_prediction", "children"),
    Output("town_A_town_heroes", "data"),
    Output("town_A_town_heroes", "columns"),
    Input("dataset_limit", "data"))
def update_town_A_town_graphs(dummy):
    sub_df = limit_df

    boxplot = bidding_boxplot(sub_df)
    heroes_data, heroes_columns = heroes_table(sub_df)

    prediction = get_optimal_player_1_bid(sub_df)
    prediction_text = f"Our model indicates the optimal bid for player 1 would be around {prediction}"

    return boxplot, prediction_text, heroes_data, heroes_columns 


# Handles the bar graph and its checkboxes and quantiles slider
@app.callback(
    Output("town_A_town_bar", "figure"),
    Output("town_A_town_bar_check", "value"),
    Output("town_A_town_bar_check_state", "data"),
    Input("town_A_town_bar_check", "value"),
    Input("town_A_town_bar_check_state", "data"),
    Input("town_A_town_bar_slider", "value"),
    Input("dataset_limit", "data"))
def update_bar_graph(value, state, quantiles, dummy):
    sub_df = limit_df

    value = list(set(value) - set(state))

    graph_value = state if value == [] else value
    graph = variable_result_graph(sub_df, graph_value[0], quantiles)
    return graph, graph_value, graph_value



if __name__ == '__main__':
    # Runs the app
    app.run_server(debug=True)