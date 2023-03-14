import dash
from dash import dcc
from dash import html
import plotly.express as px
import dash
from dash import html, dcc
import webbrowser
import pandas as pd
import dash
from dash import html, dcc, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from statistics import variance, stdev
import webbrowser
import pandas as pd
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


#read data

df = pd.read_csv("set2.csv")

castle_heroes = ['Adelaide', 'Orrin', 'Valeska', 'Edric', 'Sylvia',
                 'Beatrice', 'Lord Haart', 'Sorsha', 'Christian',
                 'Tyris', 'Rion', 'Adela', 'Cuthbert','Ingham', 'Sanya', 'Loynis',
                 'Caitlin', 'Katarzyna', 'Roland']

rampart_heroes = ['Mephala', 'Ufretin', 'Jenova', 'Ryland', 'Giselle', 'Ivor', 'Clancy', 'Thorgrim', 'Kyrre',
                  'Coronius', 'Uland', 'Elleshar', 'Gem', 'Malcom', 'Melodia', 'Alagar', 'Aeris']

tower_heroes = ['Piquedram', 'Thane', 'Josephine', 'Neela', 'Torosar', 'Fafner', 'Rissa', 'Iona', 'Astral',
                'Halon', 'Serena', 'Daremyth','Theodorus', 'Solmyr', 'Cyra', 'Aine', 'Dracon']

inferno_heroes = ['Fiona', 'Rashka', 'Marius', 'Ignatius', 'Octavia', 'Calh',
                  'Pyre', 'Nymus', 'Ayden', 'Xyron', 'Axsis', 'Olema','Calid', 'Ash', 'Zydar', 'Xarfax']

necropolis_heroes = ['Straker', 'Vokial', 'Moandor', 'Charna','Tamika', 'Isra', 'Clavius', 'Ranloo',
                     'Septienna', 'Aislinn', 'Sandro', 'Nimbus', 'Thant', 'Xsi', 'Vidomina', 'Nagash',
                    'Haart Lich', 'Galthran']

dungeon_heroes = ['Lorelei', 'lorelai', 'Arlach', 'Dace', 'Ajit', 'Damacon', 'Gunnar',
                  'Synca', 'Shakti', 'Alamar', 'Jaegar','Malekith', 'Jeddite',
                  'Deemer', 'Geon', 'Sephinroth', 'Darkstorn', 'Mutare Drake', 'Mutare']

stronghold_heroes = ['Yog', 'Gurnisson', 'Jabarkas', 'Crag Hack', 'Shiva', 'Gretchin', 'Krellion',
                     'Tyraxor', 'Gird', 'Vey', 'Dessa', 'Terek', 'Zubin', 'Gundula', 'Oris', 'Saurug', 'Boragus']

fortress_heroes = ['Bron', 'Drakon', 'Wystan', 'Tazar', 'Alkin', 'Korbac', 'Gerwulf', 'Broghild',
                   'Mirlanda', 'Rosic', 'Voy', 'Verdish', 'Kinkeria', 'Merist', 'Styg', 'Andra', 'Tiva']

conflux_heroes = ['Pasis', 'Thunar', 'Ignissa', 'Lacus', 'Kalt', 'Fiur', 'Erdamon', 'Monere',
                  'Luna', 'Inteus', 'Grindan', 'Labetha', 'Ciele', 'Gelare', 'Aenain', 'Brissa']

cove_heroes = ['Cassiopeia', 'Derek', 'Anabel', 'Illor','Tark', 'Corkes', 'Jeremy', 'Miriam', 'Elmore',
               'Leena', 'Eovacius','Astra', 'Andal', 'Manfred', 'Casmetra', 'Zilare', 'Spint', 'Dargem', 'Bidley']

towns = ["castle", "rampart", "tower", "inferno", "necropolis", "dungeon", "stronghold", "fortress", "conflux", "cove"]
heroes = {"castle": castle_heroes, "rampart": rampart_heroes, "tower": tower_heroes, "inferno": inferno_heroes,
          "necropolis": necropolis_heroes, "dungeon": dungeon_heroes, "stronghold": stronghold_heroes,
          "fortress": fortress_heroes, "conflux": conflux_heroes, "cove": cove_heroes}

if False:
    df = pd.DataFrame(columns=["result", "town", "hero", "color", "bidding", "opponent_town", "opponent_hero", "turns", "template"])

    for row in df.iterrows():
        row = row[1]
        if row[1] > row[3]: result = 1
        elif row[1] < row[3]: result = 0
        else: result = 0.5
        df_temp = pd.DataFrame([[result, row[12], row[6], row[13], row[8] , row[14], row[7], row[11], row[5]]],
                              columns = ["result", "town", "hero", "color", "bidding", "opponent_town", "opponent_hero", "turns", "template"])
        df = pd.concat([df2, df_temp])

        df_temp = pd.DataFrame([[1-result, row[14], row[7], {"red": "blue", "blue": "red", "white": "white"}[row[13]],
                                 -row[8], row[12], row[6],row[11], row[5]]],
                               columns = ["result", "town", "hero", "color", "bidding", "opponent_town", "opponent_hero", "turns", "template"])
        df = pd.concat([df, df_temp])

    df.to_csv("set2.csv", index = False)

    df = pd.read_csv("set2.csv")

    default = {}
    for town in towns:
        subset = df[(df["town"] == town) & (df2["opponent_town"] == town)]
        default[town] = subset["bidding"].abs().mean()

    res = {}
    for town in towns:
        for op_town in towns:
            subset = df[(df2["town"] == town) & (df["opponent_town"] == op_town)]
            res[town + op_town] = subset["bidding"].abs().mean() - default[town]

    print(res)

# Create the app and set the theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the first dropdown menu for selecting the template
template_options = [{'label': 'h3dm1/3', 'value': 'h3dm1/3'}, {'label': 'Nostalgia/TP', 'value': 'Nostalgia/TP'},
 {'label': '6lm10a/tp', 'value': '6lm10a/tp'}, {'label': 'mt_MP', 'value': 'mt_MP'}, {'label': 'mt_Antares', 'value': 'mt_Antares'},
 {'label': 'w/o', 'value': 'w/o'}, {'label': 'Rally', 'value': 'Rally'}, {'label': 'Spider', 'value': 'Spider'},
 {'label': 'mt_Firewalk', 'value': 'mt_Firewalk'}, {'label': 'Jebus Cross', 'value': 'Jebus Cross'}, 
 {'label': 'mt_JebusKing', 'value': 'mt_JebusKing'}, {'label': 'Duel', 'value': 'Duel'}, {'label': '8mm6a', 'value': '8mm6a'}, {'label': 'mt_Wrzosy', 'value': 'mt_Wrzosy'},
 {'label': 'mt_Andromeda', 'value': 'mt_Andromeda'}, {'label': 'Mini-nostalgia', 'value': 'Mini-nostalgia'}, {'label': '2sm4d(3)', 'value': '2sm4d(3)'}, {'label': 'Sapphire', 'value': 'Sapphire'}]
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
        dbc.Col(html.H3('Section 1'), width=12),
        dbc.Col([
            dcc.Dropdown(id='town-dropdown', options=[], value=None, style={'width': '50%'}),
            dcc.Graph(id='heroes-graph'),
            dcc.Graph(id='winrate-bidding-graph')
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col(html.H3('Section 2'), width=12),
        dbc.Col([
            dcc.Graph(id='matchup-heatmap')
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col(html.H3('Section 3'), width=12),
        dbc.Col([
            dcc.Dropdown(id='town1-dropdown', options=[], value=None, style={'width': '50%'}),
            dcc.Dropdown(id='town2-dropdown', options=[], value=None, style={'width': '50%'}),
            dcc.Graph(id='bidding-stats-graph'),
            dcc.Graph(id='scatter-plot-graph'),
            html.Ul(id='heroes-list')
        ], width=12),
    ])
])

# Define the callback for updating the dropdown menus based on the selected template
@app.callback(
    [Output('town-dropdown', 'options'),
     Output('town-dropdown', 'value'),
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
    [Output('heroes-graph', 'figure'),
     Output('winrate-bidding-graph', 'figure')],
    [Input('town-dropdown', 'value')]
)
def update_section1(town):
    # Filter data based on the selected town
    town_df = df[df['town'] == town]

    # Create the heroes graph
    heroes_fig = px.bar(town_df, x='hero', y='winrate', color='bidding')

    # Create the winrate-bidding graph
    town_df['winrate-bidding'] = town_df['winrate'] / (town_df['bidding'] / town_df['turns'])
    winrate_bidding_fig = px.bar(town_df, x='hero', y='winrate-bidding')

    return heroes_fig, winrate_bidding_fig

@app.callback(
    Output('matchup-heatmap', 'figure'),
    [Input('template-dropdown', 'value')]
)
def update_section2(template_name):
    # Filter data based on the selected template
    template_df = df[df['template_name'] == template_name]

    # Pivot the data to create the heatmap
    heatmap_df = template_df.pivot_table(index='town', columns='opponent_town', values='winrate-bidding')

    # Create the heatmap
    heatmap_fig = px.imshow(heatmap_df, color_continuous_scale='RdBu_r')

    return heatmap_fig

@app.callback(
    [Output('bidding-stats-graph', 'figure'),
     Output('scatter-plot-graph', 'figure'),
     Output('heroes-list', 'children')],
    [Input('town1-dropdown', 'value'),
     Input('town2-dropdown', 'value')]
)
def update_section3(town1, town2):
    # Filter data based on the selected towns
    town1_df = df[df['town'] == town1]
    town2_df = df[df['town'] == town2]

    # Create the bidding stats graph
    bidding_stats_df = pd.DataFrame({'Town 1': town1_df['bidding'], 'Town 2': town2_df['bidding']})
    bidding_stats_fig = px.box(bidding_stats_df, title='Bidding Statistics', color_discrete_sequence=['#1f77b4', '#ff7f0e'])
    bidding_stats_fig.update_xaxes(title='Town')
    bidding_stats_fig.update_yaxes(title='Bidding')

    # Create the scatter plot
    scatter_df = pd.concat([town1_df, town2_df])
    scatter_fig = px.scatter(scatter_df, x='winrate', y='bidding', color='town', hover_name='hero', title='Winrate vs. Bidding')
    scatter_fig.update_xaxes(title='Winrate')
    scatter_fig.update_yaxes(title='Bidding')

    # Create the heroes list
    heroes_df = pd.concat([town1_df, town2_df])
    heroes_df = heroes_df[['hero', 'winrate', 'bidding', 'pickrate']]
    heroes_df = heroes_df.sort_values(by='winrate', ascending=False)
    heroes_list = []
    for i, row in heroes_df.iterrows():
        heroes_list.append(html.Li(f"{row['hero']} - Winrate: {row['winrate']}, Bidding: {row['bidding']}, Pickrate: {row['pickrate']}"))

    return bidding_stats_fig, scatter_fig, heroes_list

if __name__ == '__main__':
    app.run_server(debug=True)


