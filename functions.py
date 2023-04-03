import os
os.environ["OMP_NUM_THREADS"] = "1"

from random import random
from statistics import stdev
from sklearn.cluster import KMeans
from copy import copy, deepcopy

import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Defines for each town their heroes, as well as the default order of those heroes
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

# Defines the default order of the heroes
towns = ["castle", "rampart", "tower", "inferno", "necropolis", "dungeon", "stronghold", "fortress", "conflux", "cove"]
heroes_per_town = {"castle": castle_heroes, "rampart": rampart_heroes, "tower": tower_heroes, "inferno": inferno_heroes,
                   "necropolis": necropolis_heroes, "dungeon": dungeon_heroes, "stronghold": stronghold_heroes,
                   "fortress": fortress_heroes, "conflux": conflux_heroes, "cove": cove_heroes}

# Makes all hero names lowercase
for town in heroes_per_town:
    heroes_per_town[town] = [hero.lower() for hero in heroes_per_town[town]]


# Full list of all heroes
full_heroes = sum([heroes_per_town[i] for i in heroes_per_town], [])

template_types = ["XL+U", "Mirror", "Jebus", "Duel", "Other"]

# Creates the table used for the winrates matchup heatmap
def town_v_town_winrate_heatmap(int_df):
    res = []
    for town in towns[::-1]:
        res.append([])
        for op_town in towns[::-1]:
            subset = int_df[(int_df["town"] == town) & (int_df["opponent_town"] == op_town)]
            if (len(subset) < 8) or ((town == op_town) and (len(subset) < 16)):
                winrate = float("nan")
            else:
                winrate = round(sum(subset["result"]) / len(subset), 2)
            res[-1].append(winrate)

    return res


# Creates the table used for the mean bidding matchup heatmap
def town_v_town_bidding_heatmap(int_df):
    res = []
    for town in towns[::-1]:
        res.append([])
        for op_town in towns[::-1]:
            subset = int_df[(int_df["town"] == town) & (int_df["opponent_town"] == op_town)]
            if (len(subset) < 8) or ((town == op_town) and (len(subset) < 16)):
                bidding = float("nan")
            else:
                bidding = round(sum(subset["bidding"]) / len(subset))
            res[-1].append(bidding)

    return res


# Creates the table used for the bidding variance matchup heatmap
def town_v_town_bidding_variance_heatmap(int_df):
    res = []
    for town in towns[::-1]:
        res.append([])
        for op_town in towns[::-1]:
            subset = int_df[(int_df["town"] == town) & (int_df["opponent_town"] == op_town)]
            if (len(subset) < 8) or ((town == op_town) and (len(subset) < 16)):
                variance = float("nan")
            else:
                variance = round(stdev(subset["bidding"]))
            res[-1].append(variance)

    return res


# Creates all different heatmaps
def create_town_v_town_graphs(int_df, highlights):
    res_winrate = town_v_town_winrate_heatmap(int_df)
    res_bidding = town_v_town_bidding_heatmap(int_df)
    res_bidding_variance = town_v_town_bidding_variance_heatmap(int_df)

    # Below parts changes the text of selected squares to have '> text <' instead of 'text'
    res_winrate_text = deepcopy(res_winrate)
    res_bidding_text = deepcopy(res_bidding)
    res_bidding_variance_text = deepcopy(res_bidding_variance)

    for res in [res_winrate_text, res_bidding_text, res_bidding_variance_text]:
        for highlight in highlights:
            res[towns[::-1].index(highlight[0])][towns[::-1].index(highlight[1])] = f"> {res[towns[::-1].index(highlight[0])][towns[::-1].index(highlight[1])]} <"

    fig_winrate = go.Figure(
        data=go.Heatmap(z=res_winrate, x=towns[::-1], y=towns[::-1], text=res_winrate_text, texttemplate="%{text}", hovertemplate="Player 1: %{x}<br>Player 2: %{y}<br>Winrate: %{z}<extra></extra>"),
        layout={"xaxis_title": 'Opponent Town', "yaxis_title": 'Player Town', "title": "Town V Town winrate"})

    fig_bidding = go.Figure(
        data=go.Heatmap(z=res_bidding, x=towns[::-1], y=towns[::-1], text=res_bidding_text, texttemplate="%{text}", hovertemplate="Player 1: %{x}<br>Player 2: %{y}<br>Mean Bidding: %{z}<extra></extra>"),
        layout={"xaxis_title": 'Opponent Town', "yaxis_title": 'Player Town', "title": "Town V Town bidding"})

    fig_bidding_variance = go.Figure(
        data=go.Heatmap(z=res_bidding_variance, x=towns[::-1], y=towns[::-1], text=res_bidding_variance_text, texttemplate="%{text}", hovertemplate="Player 1: %{x}<br>Player 2: %{y}<br>Bidding Variance: %{z}<extra></extra>"),
        layout={"xaxis_title": 'Opponent Town', "yaxis_title": 'Player Town', "title": "Town V Town bidding variance"})
   
    for fig in [fig_winrate, fig_bidding, fig_bidding_variance]:
        fig.update_layout(xaxis = {"fixedrange":True}, yaxis = {"fixedrange":True}) # Disables scrolling

    return fig_winrate, fig_bidding, fig_bidding_variance


# Creates the quantiles bar graph of a certain variable
def variable_result_graph(sub_df, variable, amount_quantiles):

    # Determines the quantile limits
    quantiles = []
    for i in [i * (1 / amount_quantiles) for i in range(amount_quantiles + 1)]:
        quantiles.append(int(sub_df[variable].quantile(i)))

    # Column names
    names = [f"{quantiles[i]} <-> {quantiles[i + 1]}" for i in range(amount_quantiles)]

    # Adds a new row to signify the quantile
    for i in range(amount_quantiles):
        sub_df.loc[((sub_df[variable] >= quantiles[i]) &
                    (sub_df[variable] <= quantiles[i + 1])), f"{variable} quantiles"] = names[i]

    # Gets the winrate of each quantile
    y = []
    for i in names:
        y.append(round(sub_df[sub_df[f"{variable} quantiles"] == i]["result"].mean(), 2))

    figure = go.Figure(data=px.bar(x=names, y=y))
    figure.update_layout(xaxis = {"title": variable.capitalize()},
                         yaxis = {"title": "Winrate"},
                         title = f"Winrate Across {amount_quantiles} Different {variable.capitalize()} Quantiles")
    
    return figure


# Creates the table with data per hero
def heroes_table(sub_df):
    sub_heroes = set(sub_df["hero"])
    sub_heroes = [hero for hero in full_heroes if hero in sub_heroes]

    # Sets up the table
    table_df = pd.DataFrame(columns=["Hero", "Mean Bidding", "Winrate", "Pickrate", "Times Picked", "Mean Turns"])

    # Creates the row for all heros
    new_row = pd.DataFrame([["all", round(sub_df["bidding"].mean(), 2), round(sub_df["result"].mean(), 2), 1,
                             len(sub_df), round(sub_df["turns"].mean(), 2)]],
                           columns=["Hero", "Mean Bidding", "Winrate", "Pickrate", "Times Picked", "Mean Turns"])
    table_df = pd.concat([table_df, new_row])

    # For each hero create a row on the table
    for hero in sub_heroes:
        sub_sub_df = sub_df[sub_df["hero"] == hero]
        new_row = pd.DataFrame([[hero, round(sub_sub_df["bidding"].mean()), round(sub_sub_df["result"].mean(), 2),
                                 round(len(sub_sub_df) / len(sub_df), 2), len(sub_sub_df),
                                 round(sub_sub_df["turns"].mean(), 2)]],
                               columns=["Hero", "Mean Bidding", "Winrate", "Pickrate", "Times Picked", "Mean Turns"])
        table_df = pd.concat([table_df, new_row])

    # Limits the length of the table to not have vertical scrolling
    if len(table_df) > 23:
        table_df = table_df.sort_values(by="Times Picked", ascending=False)
        table_df = table_df.head(23)

    data = table_df.to_dict('records')
    columns = [{"name": i, "id": i} for i in table_df.columns]
    return data, columns


# Creates the jitter plot
def town_A_town_jitter(sub_df):
    y = list(sub_df["bidding"])

    # Randomly move the point along the x axis
    x = []
    for i in range(len(y)):
        x.append(1 + (random() - 0.5))

    figure = go.Figure(data=px.scatter(y=y, x=x, color=[{"0.0": "Loss", "1.0": "Victory", "0.5": "Tie"}[str(x)] for x in sub_df["result"]]))
    figure.update_layout(xaxis = {"fixedrange":True, "showgrid":False, "visible":False},
                         yaxis = {"title": "Bidding"},
                         title = "Bidding for Different Game Outcomes")

    return figure


# Makes the bidding boxplot
def bidding_boxplot(sub_df):
    figure = go.Figure(data=px.box(sub_df, y="bidding"))
    figure.update_layout(xaxis = {"fixedrange":True, "showgrid":False, "visible":False},
                         yaxis = {"title": "Bidding"},
                         title = "Bidding Boxplot")
    
    return figure


# A model which calculates the optimal amount to bid for player one in the given dataframe
# Calculates a kmeans cluster location for the people who have won and those who lost
# The location right inbetween those is theoraticly the best
def get_optimal_player_1_bid(df):
    '''plug in a town vs. town dataframe'''
    
    df_won = df[df['result'] == 1.0]
    df_lost = df[df['result'] == 0.0]
    
    X_won = np.array(df_won['bidding']).reshape(-1, 1)
    X_lost = np.array(df_lost['bidding']).reshape(-1, 1)
    
    kmeans_won = KMeans(n_clusters=1, random_state=0, n_init=2).fit(X_won)
    kmeans_lost= KMeans(n_clusters=1, random_state=0, n_init=2).fit(X_lost)
    
    optimal_value =  int((kmeans_won.cluster_centers_[0][0] + kmeans_lost.cluster_centers_[0][0])/2)
    
    return optimal_value


def run_model(town1, town2, bidding):
    return 0