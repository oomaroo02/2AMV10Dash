import dash_bootstrap_components as dbc
import dash
from dash import html, dcc, Input, Output, dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from statistics import stdev
from copy import copy
from random import random

df = pd.read_csv("combined_processed.csv")

castle_heroes = ['Adelaide', 'Orrin', 'Valeska', 'Edric', 'Sylvia',
                 'Beatrice', 'Lord Haart', 'Sorsha', 'Christian',
                 'Tyris', 'Rion', 'Adela', 'Cuthbert', 'cuttbert', 'Ingham', 'Sanya', 'Loynis',
                 'Caitlin', 'Katarzyna', 'Roland']

rampart_heroes = ['Mephala', 'Ufretin', 'Jenova', 'Ryland', 'Giselle', 'Ivor', 'Clancy', 'Thorgrim', 'Kyrre',
                  'Coronius', 'Uland', 'Elleshar', 'Gem', 'Malcom', 'Melodia', 'Alagar', 'Aeris']

tower_heroes = ['Piquedram', 'Thane', 'Josephine', 'Neela', 'Torosar', 'Fafner', 'Rissa', 'Iona', 'Astral',
                'Halon', 'Serena', 'Daremyth', 'Theodorus', 'Solmyr', 'Cyra', 'Aine', 'Dracon']

inferno_heroes = ['Fiona', 'Rashka', 'Marius', 'Ignatius', 'Octavia', 'Calh',
                  'Pyre', 'Nymus', 'Ayden', 'Xyron', 'Axsis', 'Olema', 'Calid', 'Ash', 'Zydar', 'Xarfax']

necropolis_heroes = ['Straker', 'Vokial', 'Moandor', 'Charna', 'Tamika', 'Isra', 'Clavius', 'Ranloo',
                     'Septienna', 'Aislinn', 'Sandro', 'Nimbus', 'Thant', 'Xsi', 'Vidomina', 'Nagash',
                     'Haart Lich', 'Galthran']

dungeon_heroes = ['Lorelei', 'lorelai', 'Arlach', 'Dace', 'Ajit', 'Damacon', 'Gunnar',
                  'Synca', 'Shakti', 'Alamar', 'Jaegar', 'Malekith', 'Jeddite',
                  'Deemer', 'Geon', 'Sephinroth', 'Darkstorn', 'Mutare Drake', 'Mutare']

stronghold_heroes = ['Yog', 'Gurnisson', 'Jabarkas', 'Crag Hack', 'Shiva', 'Gretchin', 'Krellion',
                     'Tyraxor', 'Gird', 'Vey', 'Dessa', 'Terek', 'Zubin', 'Gundula', 'Oris', 'Saurug', 'Boragus']

fortress_heroes = ['Bron', 'Drakon', 'Wystan', 'Tazar', 'Alkin', 'Korbac', 'Gerwulf', 'Broghild',
                   'Mirlanda', 'Rosic', 'Voy', 'Verdish', 'Kinkeria', 'Merist', 'Styg', 'Andra', 'Tiva']

conflux_heroes = ['Pasis', 'Thunar', 'Ignissa', 'Lacus', 'Kalt', 'Fiur', 'Erdamon', 'Monere',
                  'Luna', 'Inteus', 'Grindan', 'Labetha', 'Ciele', 'Gelare', 'Aenain', 'Brissa']

cove_heroes = ['Cassiopeia', 'Derek', 'Anabel', 'Illor', 'Tark', 'Corkes', 'Jeremy', 'Miriam', 'Elmore',
               'Leena', 'Eovacius', 'Astra', 'Andal', 'Manfred', 'Casmetra', 'Zilare', 'Spint', 'Dargem']

towns = ["castle", "rampart", "tower", "inferno", "necropolis", "dungeon", "stronghold", "fortress", "conflux", "cove"]
heroes_per_town = {"castle": castle_heroes, "rampart": rampart_heroes, "tower": tower_heroes, "inferno": inferno_heroes,
                   "necropolis": necropolis_heroes, "dungeon": dungeon_heroes, "stronghold": stronghold_heroes,
                   "fortress": fortress_heroes, "conflux": conflux_heroes, "cove": cove_heroes}

for town in heroes_per_town:
    heroes_per_town[town] = [hero.lower() for hero in heroes_per_town[town]]

full_heroes = sum([heroes_per_town[i] for i in heroes_per_town], [])

template_types = ["All", "XL+U", "Mirror", "Jebus", "Duel", "Other"]

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


def town_v_town_winrate_heatmap(int_df):
    res = []
    for town in towns:
        res.append([])
        for op_town in towns[::-1]:
            subset = int_df[(int_df["town"] == town) & (int_df["opponent_town"] == op_town)]
            if (len(subset) < 8) or ((town == op_town) and (len(subset) < 16)):
                winrate = float("nan")
            else:
                winrate = round(sum(subset["result"]) / len(subset), 2)
            res[-1].append(winrate)

    return res


def town_v_town_bidding_heatmap(int_df):
    res = []
    for town in towns:
        res.append([])
        for op_town in towns[::-1]:
            subset = int_df[(int_df["town"] == town) & (int_df["opponent_town"] == op_town)]
            if (len(subset) < 8) or ((town == op_town) and (len(subset) < 16)):
                bidding = float("nan")
            else:
                bidding = round(sum(subset["bidding"]) / len(subset))
            res[-1].append(bidding)

    return res


def town_v_town_bidding_variance_heatmap(int_df):
    res = []
    for town in towns:
        res.append([])
        for op_town in towns[::-1]:
            subset = int_df[(int_df["town"] == town) & (int_df["opponent_town"] == op_town)]
            if (len(subset) < 8) or ((town == op_town) and (len(subset) < 16)):
                variance = float("nan")
            else:
                variance = round(stdev(subset["bidding"]))
            res[-1].append(variance)

    return res


def create_town_v_town_graphs(int_df):
    res_winrate = town_v_town_winrate_heatmap(int_df)
    res_bidding = town_v_town_bidding_heatmap(int_df)
    res_bidding_variance = town_v_town_bidding_variance_heatmap(int_df)

    fig_winrate = go.Figure(
        data=go.Heatmap(z=res_winrate, x=towns[::-1], y=towns, text=res_winrate, texttemplate="%{text}"),
        layout={"xaxis_title": 'Opponent Town', "yaxis_title": 'Player Town', "title": "Town V Town winrate"})

    fig_bidding = go.Figure(
        data=go.Heatmap(z=res_bidding, x=towns[::-1], y=towns, text=res_bidding, texttemplate="%{text}"),
        layout={"xaxis_title": 'Opponent Town', "yaxis_title": 'Player Town', "title": "Town V Town bidding"})

    fig_bidding_variance = go.Figure(
        data=go.Heatmap(z=res_bidding_variance, x=towns[::-1], y=towns, text=res_bidding_variance,
                        texttemplate="%{text}"),
        layout={"xaxis_title": 'Opponent Town', "yaxis_title": 'Player Town', "title": "Town V Town bidding variance"})

    return fig_winrate, fig_bidding, fig_bidding_variance


def variable_result_graph(sub_df, variable, amount_quantiles):
    quantiles = []
    for i in [i * (1 / amount_quantiles) for i in range(amount_quantiles + 1)]:
        quantiles.append(sub_df[variable].quantile(i))

    names = [f"{quantiles[i]} <-> {quantiles[i + 1]}" for i in range(amount_quantiles)]
    for i in range(amount_quantiles):
        sub_df.loc[((sub_df[variable] >= quantiles[i]) &
                    (sub_df[variable] <= quantiles[i + 1])), f"{variable} quantiles"] = names[i]

    # sub_df.loc[sub_df["bidding"] <= 0, "bidding quantiles"] = np.nan
    # sub_df.loc[sub_df["color"] == "blue", "turns quantiles"] = np.nan

    y = []
    for i in names:
        y.append(round(sub_df[sub_df[f"{variable} quantiles"] == i]["result"].mean(), 2))

    return px.bar(x=names, y=y)


def heroes_table(sub_df):
    sub_heroes = set(sub_df["hero"])
    sub_heroes = [hero for hero in full_heroes if hero in sub_heroes]

    table_df = pd.DataFrame(
        columns=["hero", "mean bidding", "winrate", "pickrate for town", "times picked", "mean turns"])
    new_row = pd.DataFrame([["all", round(sub_df["bidding"].mean(), 2), round(sub_df["result"].mean(), 2), 1,
                             len(sub_df), round(sub_df["turns"].mean(), 2)]],
                           columns=["hero", "mean bidding", "winrate", "pickrate for town", "times picked",
                                    "mean turns"])
    table_df = pd.concat([table_df, new_row])

    for hero in sub_heroes:
        sub_sub_df = sub_df[sub_df["hero"] == hero]
        new_row = pd.DataFrame([[hero, round(sub_sub_df["bidding"].mean()), round(sub_sub_df["result"].mean(), 2),
                                 round(len(sub_sub_df) / len(sub_df), 2), len(sub_sub_df),
                                 round(sub_sub_df["turns"].mean(), 2)]],
                               columns=["hero", "mean bidding", "winrate", "pickrate for town", "times picked",
                                        "mean turns"])
        table_df = pd.concat([table_df, new_row])

    data = table_df.to_dict('records')
    columns = [{"name": i, "id": i} for i in table_df.columns]
    return data, columns


def town_A_town_jitter(sub_df):
    y = list(sub_df["bidding"])

    x = []
    for i in range(len(y)):
        x.append(1 + (random() - 0.5))

    return go.Figure(data=px.scatter(y=y, x=x, color=list(sub_df["result"])))

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
