# pip install dash plotly pandas
import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import pandas as pd
import json
from datetime import datetime

# Initialize Dash app
app = dash.Dash(__name__)

# Layout with 6 real-time graphs
app.layout = html.Div([
    html.H1("🚀 Real-Time Propeller Dashboard", style={'textAlign': 'center'}),

    # Metrics row
    html.Div(id='metrics-row', style={'display': 'flex', 'justify-content': 'space-around'}),

    # Graphs in 2 rows of 3
    html.Div([
        html.Div([
            dcc.Graph(id='power-graph'),
            dcc.Graph(id='voltage-graph'), 
            dcc.Graph(id='sound-graph')
        ], style={'display': 'flex'}),

        html.Div([
            dcc.Graph(id='torque-graph'),
            dcc.Graph(id='rpm-graph'),
            dcc.Graph(id='vibrations-graph')
        ], style={'display': 'flex'})
    ]),

    # Auto-refresh component
    dcc.Interval(
        id='interval-component',
        interval=1000,  # Update every second
        n_intervals=0
    ),

    # Store component for data sharing
    dcc.Store(id='data-store')
])

# Single callback to load data (eliminates redundant CSV reads)
@callback(Output('data-store', 'data'), Input('interval-component', 'n_intervals'))
def update_data_store(n):
    try:
        df = pd.read_csv('data.csv')
        return df.to_dict('records')
    except FileNotFoundError:
        return []

# Create individual graph callbacks that use shared data
def create_graph_callback(graph_id, column, color, title):
    @callback(
        Output(f'{graph_id}', 'figure'),
        Input('data-store', 'data')
    )
    def update_graph(data):
        if not data:
            return {'data': [], 'layout': {'title': f'{title} - Waiting for data'}}

        df = pd.DataFrame(data)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[column],
            mode='lines',
            fill='tonexty',
            line=dict(color=color),
            name=title
        ))
        fig.update_layout(
            title=title,
            xaxis_title='Time (s)',
            yaxis_title=column,
            height=300
        )
        return fig
    return update_graph

# Register all graph callbacks
create_graph_callback('power-graph', 'Power', 'blue', 'Power (W)')
create_graph_callback('voltage-graph', 'Voltage', 'orange', 'Voltage (V)')
create_graph_callback('sound-graph', 'Sound', 'green', 'Sound (dB)')
create_graph_callback('torque-graph', 'Torque', 'purple', 'Torque (Nm)')
create_graph_callback('rpm-graph', 'rpm', 'red', 'RPM')
create_graph_callback('vibrations-graph', 'Vibrations', 'pink', 'Vibrations (Hz)')

# Metrics callback
@callback(Output('metrics-row', 'children'), Input('data-store', 'data'))
def update_metrics(data):
    if not data:
        return []

    df = pd.DataFrame(data)
    latest = df.iloc[-1]

    return [
        html.Div([html.H3(f"{latest['Power']} W"), html.P("Power")], style={'textAlign': 'center'}),
        html.Div([html.H3(f"{latest['Voltage']} V"), html.P("Voltage")], style={'textAlign': 'center'}),
        html.Div([html.H3(f"{latest['Sound']} dB"), html.P("Sound")], style={'textAlign': 'center'}),
        html.Div([html.H3(f"{latest['Torque']} Nm"), html.P("Torque")], style={'textAlign': 'center'}),
        html.Div([html.H3(f"{latest['rpm']} rpm"), html.P("RPM")], style={'textAlign': 'center'}),
        html.Div([html.H3(f"{latest['Vibrations']} Hz"), html.P("Vibrations")], style={'textAlign': 'center'})
    ]

if __name__ == '__main__':
    app.run_server(debug=True)