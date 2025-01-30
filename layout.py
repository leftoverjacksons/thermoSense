from dash import html, dcc
from config import COLORS

def create_layout():
    return html.Div([
        # Header Image Container
        html.Div([
            html.Img(
                src='/assets/titleblock.png' ,  # Placeholder image with 800x100 dimensions
                style={
                    'width': '800px',  # Fixed width
                    'height': '100px',  # Fixed height
                    'objectFit': 'contain',
                    'display': 'block',
                    'margin': '0',
                }
            )
        ], style={
            'backgroundColor': COLORS['background'],  # Match the dark background
            'padding': '20px',
            'display': 'flex',
            'justifyContent': 'flex-start',
            'alignItems': 'center',
            'width': '100%',
        }),
        
        # Graphs Container
        html.Div([
            # Main Graph
            dcc.Graph(
                id='live-graph',
                style={
                    'height': '300px',
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
        
        # Interval component for updates
        dcc.Interval(
            id='graph-update',
            interval=500,  # Change from 100ms to 500ms to reduce browser load with larger dataset
            n_intervals=0
        )
    ], style={
        'backgroundColor': COLORS['background'],
        'margin': '0px',
        'padding': '20px',
        'minHeight': '100vh'  # Ensure full viewport height
    })