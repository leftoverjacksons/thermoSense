### layout.py ###
from dash import html, dcc
from config import COLORS

def create_layout():
    return html.Div([
        html.H1(
            'Pressure Sensor Monitoring',
            style={
                'textAlign': 'center',
                'color': COLORS['text'],
                'fontFamily': 'Arial',
                'padding': '20px',
                'backgroundColor': COLORS['paper'],
                'margin': '0px',
                'borderRadius': '5px'
            }
        ),
        
        html.Div([
            dcc.Graph(
                id='live-graph',
                style={
                    'height': '800px',
                    'backgroundColor': COLORS['background'],
                    'padding': '20px',
                    'borderRadius': '5px'
                }
            ),
        ], style={
            'backgroundColor': COLORS['background'],
            'padding': '20px',
            'margin': '20px',
            'borderRadius': '10px',
            'boxShadow': '0px 0px 10px rgba(0,0,0,0.5)'
        }),
        
        dcc.Interval(
            id='graph-update',
            interval=100,
            n_intervals=0
        )
    ], style={'backgroundColor': COLORS['background'], 'margin': '0px', 'padding': '20px'})