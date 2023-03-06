import dash
from dash import dcc
from dash import html
import plotly.express as px

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.Div(children=[
        dcc.Dropdown(
            id='vis-model-dropdown',
            options=[
                {'label': 'Visualization Model 1', 'value': 'vis_model_1'},
                {'label': 'Visualization Model 2', 'value': 'vis_model_2'},
                {'label': 'Visualization Model 3', 'value': 'vis_model_3'}
            ],
            value='vis_model_1'
        )
    ], className='six columns'),

    html.Div(children=[
        dcc.Dropdown(
            id='ml-model-dropdown',
            options=[
                {'label': 'Machine Learning Model 1', 'value': 'ml_model_1'},
                {'label': 'Machine Learning Model 2', 'value': 'ml_model_2'},
                {'label': 'Machine Learning Model 3', 'value': 'ml_model_3'}
            ],
            value='ml_model_1'
        )
    ], className='six columns')
])

if __name__ == '__main__':
    app.run_server(debug=True)
#