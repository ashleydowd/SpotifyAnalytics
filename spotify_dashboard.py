"""
Spotify Dashboard Testing 
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('spotify.csv')

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# pandas dataframe to html table
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = dash.Dash(__name__, external_stylesheets=stylesheet)

fig = px.bar(df, x="track_name", y="energy", color="album_name")

app.layout = html.Div([
    html.H1('Spotify Analytics',
            style={'textAlign' : 'center'}),
    html.A('Click here to go to Spotify',
           href='https://www.spotify.com/us/',
           target='_blank'),
    html.P('This dashboard retrieves all of the albums and their associated data from Spotify for a given artist. Machine Gun Kelly is the current artist. Results can be filtered by the name of the album, displaying information such as danceability and loudness.',
           style={'textAlign' : 'center'}),
    dcc.Graph(figure=fig, id='energy_plot'),
    html.Div([html.H4('Albums to Display:'),
              dcc.Checklist(
                  options=[{'label': 'Lace Up (Deluxe)', 'value': 'Lace Up (Deluxe)'},
                           {'label': 'General Admission', 'value': 'General Admission'},
                           {'label': 'bloom', 'value': 'bloom'},
                           {'label': 'BINGE', 'value': 'BINGE'},
                           {'label': 'Hotel Diablo', 'value': 'Hotel Diablo'},
                           {'label': 'Tickets To My Downfall (SOLD OUT Deluxe)', 'value': 'Tickets To My Downfall (SOLD OUT Deluxe)'}],
                  value=['General Admission', 'Hotel Diablo', 'Tickets To My Downfall (SOLD OUT Deluxe)'],
                  id = 'album_checklist')],
             style={'width':'49%', 'float' : 'right'}),
    html.Div(id='table_div')
    ])

@app.callback(
    Output(component_id="table_div", component_property="children"),
    [Input(component_id="album_checklist", component_property="value")]
)
def update_table(albums):
    x = df[df.album_name.isin(albums)].sort_values('album_name')
    return generate_table(x)

@app.callback(
    Output(component_id="energy_plot", component_property="figure"),
    [Input(component_id="album_checklist", component_property="value")]
)
def update_plot(albums):
    df2 = df[df.album_name.isin(albums)].sort_values('energy', ascending=False)
    fig = px.bar(df2, x="track_name", y="energy", color="album_name")
    return fig

server = app.server

if __name__ == '__main__':
    app.run_server(debug=False)