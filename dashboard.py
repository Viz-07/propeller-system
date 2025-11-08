# dashboard.py - SIMPLE WORKING DASHBOARD
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
from data_gen import RealTimeDataStreamer

# Start data generator
streamer = RealTimeDataStreamer()
streamer.start_streaming()

# Create dash app
app = dash.Dash(__name__)

# Simple layout
app.layout = html.Div([
    html.H1("Real-Time Dashboard", style={'textAlign': 'center'}),

    # Metrics
    html.Div(id='metrics', style={'textAlign': 'center', 'fontSize': '20px', 'marginBottom': '20px'}),

    # Graphs
    html.Div([
        dcc.Graph(id='power-graph', style={'display': 'inline-block', 'width': '33%'}),
        dcc.Graph(id='voltage-graph', style={'display': 'inline-block', 'width': '33%'}),
        dcc.Graph(id='sound-graph', style={'display': 'inline-block', 'width': '33%'}),
    ]),
    html.Div([
        dcc.Graph(id='torque-graph', style={'display': 'inline-block', 'width': '33%'}),
        dcc.Graph(id='rpm-graph', style={'display': 'inline-block', 'width': '33%'}),
        dcc.Graph(id='vibrations-graph', style={'display': 'inline-block', 'width': '33%'}),
    ]),

    # Auto-refresh
    dcc.Interval(id='interval', interval=1000, n_intervals=0)
])

# Update metrics
@app.callback(Output('metrics', 'children'), Input('interval', 'n_intervals'))
def update_metrics(n):
    latest = streamer.get_latest_point()
    if not latest:
        return "Waiting for data..."

    return f"Power: {latest['Power']}W | Voltage: {latest['Voltage']}V | Sound: {latest['Sound']}dB | Torque: {latest['Torque']}Nm | RPM: {latest['rpm']} | Vibrations: {latest['Vibrations']}Hz"

# Create simple graphs
def make_figure(data, column, color):
    if not data:
        return go.Figure()

    x = [d['x_value'] for d in data]
    y = [d[column] for d in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color=color, width=2)))
    fig.update_layout(
        title=column,
        xaxis_title='Time',
        yaxis_title=column,
        height=250,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

@app.callback(Output('power-graph', 'figure'), Input('interval', 'n_intervals'))
def update_power(n):
    return make_figure(streamer.get_latest_data(), 'Power', 'blue')

@app.callback(Output('voltage-graph', 'figure'), Input('interval', 'n_intervals'))
def update_voltage(n):
    return make_figure(streamer.get_latest_data(), 'Voltage', 'orange')

@app.callback(Output('sound-graph', 'figure'), Input('interval', 'n_intervals'))
def update_sound(n):
    return make_figure(streamer.get_latest_data(), 'Sound', 'green')

@app.callback(Output('torque-graph', 'figure'), Input('interval', 'n_intervals'))
def update_torque(n):
    return make_figure(streamer.get_latest_data(), 'Torque', 'purple')

@app.callback(Output('rpm-graph', 'figure'), Input('interval', 'n_intervals'))
def update_rpm(n):
    return make_figure(streamer.get_latest_data(), 'rpm', 'red')

@app.callback(Output('vibrations-graph', 'figure'), Input('interval', 'n_intervals'))
def update_vibrations(n):
    return make_figure(streamer.get_latest_data(), 'Vibrations', 'pink')

if __name__ == '__main__':
    print("🚀 Dashboard starting at http://127.0.0.1:8050")
    app.run(debug=False, port=8050)