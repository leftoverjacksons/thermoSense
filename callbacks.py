from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from config import COLORS

def register_callbacks(app, monitor):
    @app.callback(
        Output('live-graph', 'figure'),
        [Input('graph-update', 'n_intervals')]
    )
    def update_graph(n):
        monitor.read_serial()
        
        fig = make_subplots(
            rows=2, 
            cols=1,
            subplot_titles=(
                '<b>Voltage Reading</b>',
                '<b>Pressure Reading</b>'
            ),
            vertical_spacing=0.15
        )
        
        # Add voltage trace
        fig.add_trace(
            go.Scatter(
                y=list(monitor.voltage_data),
                mode='lines',
                name='Voltage',
                line=dict(
                    color=COLORS['voltage'],
                    width=3,
                    shape='spline'
                ),
                fill='tozeroy',
                fillcolor=f'rgba(0, 255, 0, 0.1)'
            ),
            row=1, col=1
        )
        
        # Add pressure trace
        fig.add_trace(
            go.Scatter(
                y=list(monitor.pressure_data),
                mode='lines',
                name='Pressure',
                line=dict(
                    color=COLORS['pressure'],
                    width=3,
                    shape='spline'
                ),
                fill='tozeroy',
                fillcolor=f'rgba(255, 68, 68, 0.1)'
            ),
            row=2, col=1
        )
        
        # Update layout
        fig.update_layout(
            height=800,
            showlegend=True,
            paper_bgcolor=COLORS['paper'],
            plot_bgcolor=COLORS['background'],
            font=dict(color=COLORS['text']),
            margin=dict(l=50, r=50, t=30, b=30),
            legend=dict(
                bgcolor=COLORS['paper'],
                bordercolor=COLORS['text'],
                borderwidth=1
            ),
            title_font=dict(size=24),
        )
        
        # Update axes styling
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor=COLORS['grid'],
            zeroline=False,
            showline=True,
            linewidth=2,
            linecolor=COLORS['grid']
        )
        
        # Set dynamic ranges
        voltage_range = [0, max(5.0, monitor.max_voltage * 1.1)]
        pressure_range = [0, max(200.0, monitor.max_pressure * 1.1)]
        
        fig.update_yaxes(
            title_text='Voltage (V)',
            range=voltage_range,
            row=1, col=1,
            showgrid=True,
            gridwidth=1,
            gridcolor=COLORS['grid'],
            zeroline=False,
            showline=True,
            linewidth=2,
            linecolor=COLORS['grid']
        )
        
        fig.update_yaxes(
            title_text='Pressure (PSI)',
            range=pressure_range,
            row=2, col=1,
            showgrid=True,
            gridwidth=1,
            gridcolor=COLORS['grid'],
            zeroline=False,
            showline=True,
            linewidth=2,
            linecolor=COLORS['grid']
        )
        
        # Add annotations
        if monitor.voltage_data and monitor.pressure_data:
            latest_voltage = monitor.voltage_data[-1]
            latest_pressure = monitor.pressure_data[-1]
            
            fig.add_annotation(
                text=f"<b>Current: {latest_voltage:.3f}V</b><br>Max: {monitor.max_voltage:.3f}V",
                xref="paper", yref="paper",
                x=1.02, y=0.5,
                xanchor="left",
                font=dict(size=16, color=COLORS['voltage']),
                showarrow=False,
                row=1, col=1
            )
            
            fig.add_annotation(
                text=f"<b>Current: {latest_pressure:.1f}PSI</b><br>Max: {monitor.max_pressure:.1f}PSI",
                xref="paper", yref="paper",
                x=1.02, y=0.0,
                xanchor="left",
                font=dict(size=16, color=COLORS['pressure']),
                showarrow=False,
                row=2, col=1
            )
        
        return fig