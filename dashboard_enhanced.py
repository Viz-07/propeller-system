import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
from data_gen import RealTimeDataStreamer

"""
import logging

# Suppress Flask logging (keep terminal clean)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
"""

sensor = RealTimeDataStreamer()
sensor.start_streaming()
app = dash.Dash(__name__)

COLORS = {
    'background': '#0f172a',
    'text': '#f1f5f9',
    'text_secondary': '#94a3b8',
    'power': '#3b82f6',
    'voltage': '#f59e0b',
    'sound': '#10b981',
    'torque': '#8b5cf6',
    'rpm': '#ef4444',
    'vibrations': '#ec4899',
    'accent': '#06b6d4'
}

app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Real-Time Propeller Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                margin: 0;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                color: #f1f5f9;
            }
            .metric-card {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 12px;
                padding: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                transition: all 0.3s ease;
            }
            .metric-card:hover {
                background: rgba(255, 255, 255, 0.08);
                transform: translateY(-2px);
            }
            .download-btn {
                background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            .download-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(6, 182, 212, 0.3);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1('🚀 Real-Time Propeller Dashboard', 
                   style={'margin': 0, 'fontSize': '28px', 'fontWeight': '700'}),
            html.Div([
                html.Span('🟢 LIVE', style={
                    'background': 'rgba(16, 185, 129, 0.2)',
                    'color': '#10b981',
                    'padding': '5px 15px',
                    'borderRadius': '20px',
                    'fontSize': '14px',
                    'fontWeight': '600',
                    'marginRight': '10px'
                }),
                html.Button('⬇️ Download CSV', id='download-btn', n_clicks=0, 
                           style={
                               'background': 'linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%)',
                               'color': 'white',
                               'padding': '10px 20px',
                               'borderRadius': '8px',
                               'border': 'none',
                               'cursor': 'pointer',
                               'fontWeight': '600'
                           })
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'})
    ], style={
        'padding': '20px 40px',
        'background': 'rgba(255, 255, 255, 0.05)',
        'borderBottom': '1px solid rgba(255, 255, 255, 0.1)'
    }),

    dcc.Download(id='download-csv'),

    html.Div(id='metrics-row', style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fit, minmax(180px, 1fr))',
        'gap': '15px',
        'padding': '20px 40px'
    }),

    html.Div([
        html.Div([dcc.Graph(id='power-graph', config={'displayModeBar': False})], style={'padding': '10px'}),
        html.Div([dcc.Graph(id='voltage-graph', config={'displayModeBar': False})], style={'padding': '10px'}),
        html.Div([dcc.Graph(id='sound-graph', config={'displayModeBar': False})], style={'padding': '10px'}),
        html.Div([dcc.Graph(id='torque-graph', config={'displayModeBar': False})], style={'padding': '10px'}),
        html.Div([dcc.Graph(id='rpm-graph', config={'displayModeBar': False})], style={'padding': '10px'}),
        html.Div([dcc.Graph(id='vibrations-graph', config={'displayModeBar': False})], style={'padding': '10px'}),
    ], style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(3, 1fr)',
        'gap': '0px',
        'padding': '0 30px'
    }),

    html.Div([
        html.H2('📊 Custom Comparison', style={
            'fontSize': '22px',
            'fontWeight': '600',
            'marginBottom': '20px',
            'color': COLORS['text']
        }),
        html.Div([
            html.Div([
                html.Label('X-Axis:', style={'marginRight': '10px', 'fontWeight': '500', 'color': COLORS['text']}),
                dcc.Dropdown(
                    id='x-axis-dropdown',
                    options=[
                        {'label': '⚡ Power', 'value': 'Power'},
                        {'label': '🔋 Voltage', 'value': 'Voltage'},
                        {'label': '🔊 Sound', 'value': 'Sound'},
                        {'label': '⚙️ Torque', 'value': 'Torque'},
                        {'label': '🔄 RPM', 'value': 'rpm'},
                        {'label': '〰️ Vibrations', 'value': 'Vibrations'}
                    ],
                    value='Power',
                    style={'width': '200px', 'color': '#000'}
                )
            ], style={'display': 'flex', 'alignItems': 'center', 'marginRight': '30px'}),
            html.Div([
                html.Label('Y-Axis:', style={'marginRight': '10px', 'fontWeight': '500', 'color': COLORS['text']}),
                dcc.Dropdown(
                    id='y-axis-dropdown',
                    options=[
                        {'label': '⚡ Power', 'value': 'Power'},
                        {'label': '🔋 Voltage', 'value': 'Voltage'},
                        {'label': '🔊 Sound', 'value': 'Sound'},
                        {'label': '⚙️ Torque', 'value': 'Torque'},
                        {'label': '🔄 RPM', 'value': 'rpm'},
                        {'label': '〰️ Vibrations', 'value': 'Vibrations'}
                    ],
                    value='Voltage',
                    style={'width': '200px', 'color': '#000'}
                )
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], style={'display': 'flex', 'marginBottom': '20px'}),
        dcc.Graph(id='comparison-graph', config={'displayModeBar': False})
    ], style={
        'padding': '30px 40px',
        'background': 'rgba(255, 255, 255, 0.03)',
        'margin': '20px 40px',
        'borderRadius': '16px',
        'border': '1px solid rgba(255, 255, 255, 0.1)'
    }),

    html.Div([
        html.H2('📋 Latest Data (Last 10 Readings)', style={
            'fontSize': '22px',
            'fontWeight': '600',
            'marginBottom': '20px',
            'color': COLORS['text']
        }),
        html.Div(id='data-table-container')
    ], style={
        'padding': '30px 40px',
        'background': 'rgba(255, 255, 255, 0.03)',
        'margin': '20px 40px',
        'borderRadius': '16px',
        'border': '1px solid rgba(255, 255, 255, 0.1)'
    }),

    dcc.Interval(id='interval', interval=1000, n_intervals=0)

], style={'minHeight': '100vh', 'background': 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)'})

@app.callback(Output('metrics-row', 'children'), Input('interval', 'n_intervals'))
def update_metrics(n):
    latest = sensor.get_latest_point()
    if not latest:
        return []

    metrics = [
        ('⚡ Power', latest['Power'], 'W', COLORS['power']),
        ('🔋 Voltage', latest['Voltage'], 'V', COLORS['voltage']),
        ('🔊 Sound', latest['Sound'], 'dB', COLORS['sound']),
        ('⚙️ Torque', latest['Torque'], 'Nm', COLORS['torque']),
        ('🔄 RPM', latest['rpm'], 'rpm', COLORS['rpm']),
        ('〰️ Vibrations', latest['Vibrations'], 'Hz', COLORS['vibrations'])
    ]

    cards = []
    for icon_name, value, unit, color in metrics:
        card = html.Div([
            html.Div(icon_name, style={
                'fontSize': '14px',
                'color': COLORS['text_secondary'],
                'marginBottom': '8px'
            }),
            html.Div([
                html.Span(f"{value:.1f}", style={
                    'fontSize': '28px',
                    'fontWeight': '700',
                    'color': color
                }),
                html.Span(f" {unit}", style={
                    'fontSize': '16px',
                    'color': COLORS['text_secondary'],
                    'marginLeft': '5px'
                })
            ])
        ], style={
            'background': 'rgba(255, 255, 255, 0.05)',
            'borderRadius': '12px',
            'padding': '15px',
            'border': '1px solid rgba(255, 255, 255, 0.1)'
        })
        cards.append(card)

    return cards

@app.callback(Output('power-graph', 'figure'), Input('interval', 'n_intervals'))
def update_power(n):
    data = sensor.get_latest_data(50)
    if not data:
        return go.Figure()

    x = [d['x_value'] for d in data]
    y = [d['Power'] for d in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, 
        fill='tozeroy',
        mode='lines',
        line=dict(color=COLORS['power'], width=2),
        fillcolor=f"rgba(59, 130, 246, 0.3)"
    ))
    fig.update_layout(
        title='⚡ Power (W)',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.03)',
        font=dict(color=COLORS['text']),
        height=280,
        margin=dict(l=40, r=20, t=40, b=30),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    return fig

@app.callback(Output('voltage-graph', 'figure'), Input('interval', 'n_intervals'))
def update_voltage(n):
    data = sensor.get_latest_data(50)
    if not data:
        return go.Figure()

    x = [d['x_value'] for d in data]
    y = [d['Voltage'] for d in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines+markers',
        line=dict(color=COLORS['voltage'], width=2),
        marker=dict(size=4, color=COLORS['voltage'])
    ))
    fig.update_layout(
        title='🔋 Voltage (V)',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.03)',
        font=dict(color=COLORS['text']),
        height=280,
        margin=dict(l=40, r=20, t=40, b=30),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    return fig

@app.callback(Output('sound-graph', 'figure'), Input('interval', 'n_intervals'))
def update_sound(n):
    data = sensor.get_latest_data(30)
    if not data:
        return go.Figure()

    x = [d['x_value'] for d in data]
    y = [d['Sound'] for d in data]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x, y=y,
        marker=dict(color=COLORS['sound'])
    ))
    fig.update_layout(
        title='🔊 Sound (dB)',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.03)',
        font=dict(color=COLORS['text']),
        height=280,
        margin=dict(l=40, r=20, t=40, b=30),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    return fig

@app.callback(Output('torque-graph', 'figure'), Input('interval', 'n_intervals'))
def update_torque(n):
    latest = sensor.get_latest_point()
    if not latest:
        return go.Figure()

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=latest['Torque'],
        delta={'reference': 300},
        title={'text': "⚙️ Torque (Nm)"},
        gauge={
            'axis': {'range': [None, 500]},
            'bar': {'color': COLORS['torque']},
            'steps': [
                {'range': [0, 200], 'color': 'rgba(139, 92, 246, 0.2)'},
                {'range': [200, 350], 'color': 'rgba(139, 92, 246, 0.3)'},
                {'range': [350, 500], 'color': 'rgba(139, 92, 246, 0.4)'}
            ],
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']),
        height=280,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

@app.callback(Output('rpm-graph', 'figure'), Input('interval', 'n_intervals'))
def update_rpm(n):
    data = sensor.get_latest_data(50)
    if not data:
        return go.Figure()

    x = [d['x_value'] for d in data]
    y = [d['rpm'] for d in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines',
        line=dict(color=COLORS['rpm'], width=3)
    ))
    fig.update_layout(
        title='🔄 RPM',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.03)',
        font=dict(color=COLORS['text']),
        height=280,
        margin=dict(l=40, r=20, t=40, b=30),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    return fig

@app.callback(Output('vibrations-graph', 'figure'), Input('interval', 'n_intervals'))
def update_vibrations(n):
    data = sensor.get_latest_data(50)
    if not data:
        return go.Figure()

    x = [d['x_value'] for d in data]
    y = [d['Vibrations'] for d in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='markers',
        marker=dict(
            size=8,
            color=y,
            colorscale='Pinkyl',
            showscale=True,
            colorbar=dict(title="Hz")
        )
    ))
    fig.update_layout(
        title='〰️ Vibrations (Hz)',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.03)',
        font=dict(color=COLORS['text']),
        height=280,
        margin=dict(l=40, r=20, t=40, b=30),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    return fig

# Comparison Graph
@app.callback(
    Output('comparison-graph', 'figure'),
    [Input('interval', 'n_intervals'),
     Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value')]
)
def update_comparison(n, x_col, y_col):
    data = sensor.get_latest_data()

    # Handle None values
    if not data or x_col is None or y_col is None:
        return go.Figure()

    x_data = [d[x_col] for d in data]
    y_data = [d[y_col] for d in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode='markers',
        marker=dict(
            size=10,
            color=COLORS['accent'],
            opacity=0.7,
            line=dict(width=1, color='white')
        ),
        text=[f"Point {d['x_value']}" for d in data],
        hovertemplate=f'{x_col}: %{{x}}<br>{y_col}: %{{y}}<extra></extra>'
    ))
    fig.update_layout(
        title=f'{x_col} vs {y_col}',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.03)',
        font=dict(color=COLORS['text']),
        height=400,
        margin=dict(l=60, r=40, t=60, b=60),
        xaxis=dict(title=x_col, showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title=y_col, showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    return fig

@app.callback(Output('data-table-container', 'children'), Input('interval', 'n_intervals'))
def update_data_table(n):
    data = sensor.get_latest_data(10)
    if not data:
        return html.Div("No data available", style={'color': COLORS['text_secondary']})

    df = pd.DataFrame(data)

    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in df.columns],
        style_cell={
            'textAlign': 'center',
            'padding': '10px',
            'backgroundColor': 'rgba(255, 255, 255, 0.05)',
            'color': COLORS['text'],
            'border': '1px solid rgba(255, 255, 255, 0.1)'
        },
        style_header={
            'backgroundColor': 'rgba(255, 255, 255, 0.1)',
            'fontWeight': 'bold',
            'border': '1px solid rgba(255, 255, 255, 0.2)'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgba(255, 255, 255, 0.02)'
            }
        ]
    )

# CSV Download
@app.callback(
    Output('download-csv', 'data'),
    Input('download-btn', 'n_clicks'),
    prevent_initial_call=True
)
def download_csv(n_clicks):
    if n_clicks is None or n_clicks == 0:
        return None

    data = sensor.get_latest_data()
    if not data:
        return None

    df = pd.DataFrame(data)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"propeller_data_{timestamp}.csv"

    return dcc.send_data_frame(df.to_csv, filename, index=False)


if __name__ == '__main__':
    print("✅ Data streaming started!")
    print("🚀 Dashboard starting...")
    print("📊 Open: http://127.0.0.1:8050")
    print("🔇 Terminal logging suppressed (clean output)")
    app.run(debug=False, port=8050)
