import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import pandas as pd
from data_gen import RealTimeDataStreamer

# Initialize data streamer
data_streamer = RealTimeDataStreamer(max_points=1000)
data_streamer.start_streaming()

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("⚡ Ultra-Fast Real-Time Dashboard", style={'textAlign': 'center', 'color': '#2c3e50'}),

    html.Div(id='status-indicator', style={'textAlign': 'center', 'marginBottom': '20px'}),

    # Live metrics cards
    html.Div(id='metrics-grid', style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))',
        'gap': '15px',
        'marginBottom': '30px'
    }),

    # Real-time graphs
    html.Div([
        html.Div([
            dcc.Graph(id='power-graph', config={'displayModeBar': False}),
            dcc.Graph(id='voltage-graph', config={'displayModeBar': False}),
            dcc.Graph(id='sound-graph', config={'displayModeBar': False})
        ], style={'display': 'flex', 'gap': '10px'}),

        html.Div([
            dcc.Graph(id='torque-graph', config={'displayModeBar': False}),
            dcc.Graph(id='rpm-graph', config={'displayModeBar': False}),
            dcc.Graph(id='vibrations-graph', config={'displayModeBar': False})
        ], style={'display': 'flex', 'gap': '10px'})
    ]),

    # Ultra-fast refresh (every 500ms for demonstration)
    dcc.Interval(
        id='interval-component',
        interval=500,  # Update every 0.5 seconds
        n_intervals=0
    )
], style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'})

def create_real_time_figure(data_list, column, color, title):
    """Create a plotly figure with smooth real-time updates"""
    if not data_list:
        return {'data': [], 'layout': {'title': f'{title} - No Data'}}

    x_values = [d['x_value'] for d in data_list]
    y_values = [d[column] for d in data_list]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines+markers',
        line=dict(color=color, width=3),
        marker=dict(size=4),
        name=title,
        fill='tonexty',
        fillcolor=f'rgba({color[4:-1]}, 0.1)'  # Semi-transparent fill
    ))

    fig.update_layout(
        title={'text': f'{title}: {y_values[-1]:.1f}', 'x': 0.5},
        xaxis={'title': 'Time (s)', 'showgrid': True},
        yaxis={'title': column, 'showgrid': True},
        height=300,
        margin=dict(l=50, r=50, t=50, b=50),
        plot_bgcolor='rgba(240,240,240,0.5)',
        showlegend=False
    )

    return fig

# Status callback
@callback(Output('status-indicator', 'children'), Input('interval-component', 'n_intervals'))
def update_status(n):
    data_points = len(data_streamer.data_buffer)
    latest = data_streamer.get_latest_point()

    if latest:
        return html.Div([
            html.Span(f"🟢 LIVE", style={'color': 'green', 'fontWeight': 'bold'}),
            html.Span(f" | {data_points} data points | Last update: {latest['x_value']}s"),
        ])
    return html.Div("🔴 No Data", style={'color': 'red'})

# Metrics callback
@callback(Output('metrics-grid', 'children'), Input('interval-component', 'n_intervals'))
def update_metrics(n):
    latest = data_streamer.get_latest_point()
    if not latest:
        return []

    metrics = [
        ('Power', latest['Power'], 'W', '#3498db'),
        ('Voltage', latest['Voltage'], 'V', '#e67e22'),
        ('Sound', latest['Sound'], 'dB', '#27ae60'),
        ('Torque', latest['Torque'], 'Nm', '#9b59b6'),
        ('RPM', latest['rpm'], 'rpm', '#e74c3c'),
        ('Vibrations', latest['Vibrations'], 'Hz', '#f39c12')
    ]

    cards = []
    for name, value, unit, color in metrics:
        card = html.Div([
            html.H3(f"{value:.1f}", style={'margin': '0', 'color': color}),
            html.P(f"{name} ({unit})", style={'margin': '5px 0 0 0', 'color': '#7f8c8d'})
        ], style={
            'backgroundColor': 'white',
            'padding': '20px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'border': f'3px solid {color}'
        })
        cards.append(card)

    return cards

# Graph callbacks using memory data (ultra-fast!)
graph_configs = [
    ('power-graph', 'Power', '#3498db'),
    ('voltage-graph', 'Voltage', '#e67e22'),
    ('sound-graph', 'Sound', '#27ae60'),
    ('torque-graph', 'Torque', '#9b59b6'),
    ('rpm-graph', 'rpm', '#e74c3c'),
    ('vibrations-graph', 'Vibrations', '#f39c12')
]

for graph_id, column, color in graph_configs:
    @callback(
        Output(graph_id, 'figure'),
        Input('interval-component', 'n_intervals'),
        prevent_initial_call=False
    )
    def update_graph(n, col=column, c=color, gid=graph_id):
        # Get last 50 points for smooth scrolling
        data_list = data_streamer.get_latest_data(50)
        return create_real_time_figure(data_list, col, c, col)

if __name__ == '__main__':
    try:
        print("🚀 Starting Ultra-Fast Dashboard...")
        print("📊 Dashboard will be available at: http://127.0.0.1:8050")
        app.run(debug=False, port=8050)
    finally:
        data_streamer.stop_streaming()