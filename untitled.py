import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(id='site-dropdown',
                 options=[{'label': 'All Sites', 'value': 'ALL'}] +
                         [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                    value=[min_payload, max_payload]),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

@app.callback(Output('success-pie-chart', 'figure'),
              Input('site-dropdown', 'value'))
def update_pie(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, names='Launch Site', values='class',
                     title='Total Success Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class',
                     title=f'Success vs Failure for {selected_site}')
    return fig

@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'),
               Input('payload-slider', 'value')])
def update_scatter(selected_site, payload_range):
    low, high = payload_range
    df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) &
                   (spacex_df['Payload Mass (kg)'] <= high)]
    if selected_site != 'ALL':
        df = df[df['Launch Site'] == selected_site]
    fig = px.scatter(df, x='Payload Mass (kg)', y='class',
                     color='Booster Version Category',
                     title='Payload vs. Outcome')
    return fig

if __name__ == '__main__':
    app.run()
