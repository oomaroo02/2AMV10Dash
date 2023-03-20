from random import random
import plotly.graph_objects as go
from statistics import stdev
import plotly.express as px
import pandas as pd

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

template_types = ["XL+U", "Mirror", "Jebus", "Duel", "Other"]

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



