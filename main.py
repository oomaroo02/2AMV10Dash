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

df = pd.read_csv("combined_processed.csv")

if False:
    df2 = pd.DataFrame(
        columns=["result", "town", "hero", "color", "bidding", "opponent_town", "opponent_hero", "turns", "template"])

    for row in df.iterrows():
        row = row[1]
        if row[1] > row[3]:
            result = 1
        elif row[1] < row[3]:
            result = 0
        else:
            result = 0.5
        df_temp = pd.DataFrame([[result, row[12], row[6], row[13], row[8], row[14], row[7], row[11], row[5], row[16]]],
                               columns=["result", "town", "hero", "color", "bidding", "opponent_town", "opponent_hero",
                                        "turns", "template", "template_type"])
        df2 = pd.concat([df2, df_temp])

        df_temp = pd.DataFrame([[1 - result, row[14], row[7], {"red": "blue", "blue": "red", "white": "white"}[row[13]],
                                 -row[8], row[12], row[6], row[11], row[5], row[16]]],
                               columns=["result", "town", "hero", "color", "bidding", "opponent_town", "opponent_hero",
                                        "turns", "template", "template_type"])
        df2 = pd.concat([df2, df_temp])

    df2.to_csv("set2.csv", index=False)

df2 = pd.read_csv("set2.csv")

# Create the app and set the theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the first dropdown menu for selecting the template
template_options = [{'label': 'h3dm1/3', 'value': 'h3dm1/3'}, {'label': 'Nostalgia/TP', 'value': 'Nostalgia/TP'},
                    {'label': '6lm10a/tp', 'value': '6lm10a/tp'}, {'label': 'mt_MP', 'value': 'mt_MP'},
                    {'label': 'mt_Antares', 'value': 'mt_Antares'},
                    {'label': 'w/o', 'value': 'w/o'}, {'label': 'Rally', 'value': 'Rally'},
                    {'label': 'Spider', 'value': 'Spider'},
                    {'label': 'mt_Firewalk', 'value': 'mt_Firewalk'}, {'label': 'Jebus Cross', 'value': 'Jebus Cross'},
                    {'label': 'mt_JebusKing', 'value': 'mt_JebusKing'}, {'label': 'Duel', 'value': 'Duel'},
                    {'label': '8mm6a', 'value': '8mm6a'}, {'label': 'mt_Wrzosy', 'value': 'mt_Wrzosy'},
                    {'label': 'mt_Andromeda', 'value': 'mt_Andromeda'},
                    {'label': 'Mini-nostalgia', 'value': 'Mini-nostalgia'}, {'label': '2sm4d(3)', 'value': '2sm4d(3)'},
                    {'label': 'Sapphire', 'value': 'Sapphire'}]
template_dropdown = dcc.Dropdown(id='template-dropdown', options=template_options, value=df['template'].iloc[0])

# Define the layout of the app
app.layout = html.Div([
    dbc.Row([
        dbc.Col(html.H1('Dashboard'), width=12)
    ]),
    dbc.Row([
        dbc.Col(template_dropdown, width=12)
    ]),
    dbc.Row([
        dbc.Col(html.H3('Section 2'), width=12),
        dbc.Col(
            [dcc.Dropdown(template_types, value="All", id="template_dropdown"),
             dcc.Graph(id="town_V_town_graph"),
             dcc.Checklist(options=["bidding", "win rate", "bidding variance"], value=["bidding"],
                           id="town_V_town_check"),
             dcc.Store(data=[], id="town_V_town_state"),
             dcc.Store(data=0, id="dataset")]),
    ]),
    dbc.Row([
        dbc.Col(html.H3('Section 3'), width=12),
        dbc.Col([
            dash_table.DataTable(sort_action='native', id="town_A_town_heroes"),
            dcc.Graph(id="town_A_town_boxplot"),
            dcc.Graph(id="town_A_town_jitter"),
            dcc.Graph(id="town_A_town_bar"),
            dcc.Checklist(options=["bidding", "turns"], value=["bidding"], id="town_A_town_bar_check"),
            dcc.Store(data=[], id="town_A_town_bar_check_state"),
            dcc.Slider(min=1, max=10, step=1, value=5, id='town_A_town_bar_slider'),
            dcc.Dropdown(towns, value=towns[0], id='town_A_town_dropdown_1'),
            dcc.Dropdown(["all"] + towns, value="all", id='town_A_town_dropdown_2')]),
    ])
])


# Define the callback for updating the dropdown menus based on the selected template
# Define the callback for updating the dropdown menus based on the selected template
@app.callback(
    [Output('template-dropdown', 'options'),
     Output('template-dropdown', 'value'),
     Output('town1-dropdown', 'options'),
     Output('town1-dropdown', 'value'),
     Output('town2-dropdown', 'options'),
     Output('town2-dropdown', 'value')],
    [Input('template-dropdown', 'value')]
)
def update_dropdowns(template):
    # Filter data based on the selected template
    template_df = df[df['template'] == template]

    # Update dropdown options for Section 1
    town_options = [{'label': i, 'value': i} for i in template_df['town'].unique()]
    town_value = template_df['town'].iloc[0]

    # Update dropdown options for Section 3
    town1_options = [{'label': i, 'value': i} for i in template_df['town'].unique()]
    town2_options = [{'label': i, 'value': i} for i in template_df['opponent_town'].unique()]
    town1_value = template_df['town'].iloc[0]
    town2_value = template_df['opponent_town'].iloc[0]

    return town_options, town_value, town1_options, town1_value, town2_options, town2_value


# Define the callback for updating the graphs based on the selected town in Section 1
@app.callback(
    Output("dataset", "data"),
    Input("dataset", "data"),
    Input("template_dropdown", "value"))
def update_template(cur_data, template):
    global used_df, fig_winrate, fig_bidding, fig_bidding_variance

    if template != "All":
        used_df = df2[df2["template_type"] == template]
    else:
        used_df = copy(df2)

    fig_winrate, fig_bidding, fig_bidding_variance = create_town_v_town_graphs(used_df)

    return cur_data + 1


@app.callback(
    Output("town_V_town_graph", "figure"),
    Output("town_V_town_check", "value"),
    Output("town_V_town_state", "data"),
    Input("town_V_town_check", "value"),
    Input("town_V_town_state", "data"),
    Input("dataset", "data"))
def update_section2(template, value, state, cur_data):
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
    Input("town_A_town_dropdown_2", "value"))
def town_A_town(town1, town2):
    sub_df = df2[df2["town"] == town1] if town2 == "all" else df2[
        (df2["town"] == town1) & (df2["opponent_town"] == town2)]

    boxplot = go.Figure(data=px.box(sub_df, y="bidding"))
    jitter = town_A_town_jitter(sub_df)
    heroes_data, heroes_columns = heroes_table(sub_df)

    return jitter, boxplot, heroes_data, heroes_columns


@app.callback(
    Output("town_A_town_bar", "figure"),
    Output("town_A_town_bar_check", "value"),
    Output("town_A_town_bar_check_state", "data"),
    Input("town_A_town_bar_check", "value"),
    Input("town_A_town_bar_check_state", "data"),
    Input("town_A_town_bar_slider", "value"),
    Input("town_A_town_dropdown_1", "value"),
    Input("town_A_town_dropdown_2", "value"))
def town_graph(value, state, quantiles, town1, town2):
    sub_df = df2[df2["town"] == town1] if town2 == "all" else df2[
        (df2["town"] == town1) & (df2["opponent_town"] == town2)]

    value = list(set(value) - set(state))

    graph_value = state if value == [] else value
    graph = variable_result_graph(sub_df, graph_value[0], quantiles)
    return graph, graph_value, graph_value

if __name__ == '__main__':
    app.run_server(debug=True)
