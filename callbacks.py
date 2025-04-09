from dash import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from config import COLORS

def get_heater_state_text(state):
    if state == 0:
        return "COOLING"
    elif state == 1:
        return "HEATING"
    elif state == 2:
        return "STABILIZING"
    return "UNKNOWN"

def register_callbacks(app, monitor):
    @app.callback(
        Output('live-graph', 'figure'),
        [Input('graph-update', 'n_intervals')]
    )
    def update_graph(n):
        monitor.read_serial()
        
        # Create subplots for all sensors
        fig = make_subplots(
            rows=2, 
            cols=2,
            subplot_titles=(
                '<b>Pressure Reading</b>',
                '<b>Temperature Reading</b>',
                '<b>pH Reading</b>',
                ''  # Empty subplot or additional data if needed
            ),
            horizontal_spacing=0.1,
            vertical_spacing=0.2
        )
        
        # Add pressure trace (top left)
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
            row=1, col=1
        )
        
        # Add temperature trace (top right)
        fig.add_trace(
            go.Scatter(
                y=list(monitor.temperature_data),
                mode='lines',
                name='Temperature',
                line=dict(
                    color=COLORS['temperature'],
                    width=3,
                    shape='spline'
                ),
                fill='tozeroy',
                fillcolor=f'rgba(66, 135, 245, 0.1)'
            ),
            row=1, col=2
        )
        
        # Add pH trace (bottom left)
        fig.add_trace(
            go.Scatter(
                y=list(monitor.ph_data),
                mode='lines',
                name='pH',
                line=dict(
                    color=COLORS['ph'],
                    width=3,
                    shape='spline'
                ),
                fill='tozeroy',
                fillcolor=f'rgba(147, 112, 219, 0.1)'
            ),
            row=2, col=1
        )
        
        # Update layout (existing code)
        fig.update_layout(
            height=600,  # Increase height for additional plot
            showlegend=False,
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
        
        # Update axes styling (existing code)
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
        pressure_range = [0, max(200.0, monitor.max_pressure * 1.1)]
        temp_range = [
            min(0.0, monitor.min_temperature * 0.9),
            max(50.0, monitor.max_temperature * 1.1)
        ]
        ph_range = [
            min(0.0, monitor.min_ph * 0.9),
            max(14.0, monitor.max_ph * 1.1)
        ]
        
        # Update y-axes (pressure)
        fig.update_yaxes(
            title_text='Pressure (PSI)',
            range=pressure_range,
            row=1, col=1,
            showgrid=True,
            gridwidth=1,
            gridcolor=COLORS['grid'],
            zeroline=False,
            showline=True,
            linewidth=2,
            linecolor=COLORS['grid']
        )
        
        # Update y-axes (temperature)
        fig.update_yaxes(
            title_text='Temperature (°C)',
            range=temp_range,
            row=1, col=2,
            showgrid=True,
            gridwidth=1,
            gridcolor=COLORS['grid'],
            zeroline=False,
            showline=True,
            linewidth=2,
            linecolor=COLORS['grid']
        )
        
        # Update y-axes (pH)
        fig.update_yaxes(
            title_text='pH',
            range=ph_range,
            row=2, col=1,
            showgrid=True,
            gridwidth=1,
            gridcolor=COLORS['grid'],
            zeroline=False,
            showline=True,
            linewidth=2,
            linecolor=COLORS['grid']
        )
        
        # Add annotations for current and max values
        if monitor.pressure_data and monitor.temperature_data and monitor.ph_data:
            latest_pressure = monitor.pressure_data[-1]
            latest_temp = monitor.temperature_data[-1]
            latest_ph = monitor.ph_data[-1]
            latest_heater_state = monitor.heater_states[-1] if monitor.heater_states else None
            
            # Pressure annotation
            fig.add_annotation(
                text=f"<b>Current: {latest_pressure:.1f}PSI</b><br>Max: {monitor.max_pressure:.1f}PSI",
                xref="paper", yref="paper",
                x=0.02, y=0.95,
                xanchor="left",
                font=dict(size=16, color=COLORS['pressure']),
                showarrow=False,
            )
            
            # Temperature annotation
            heater_state_text = get_heater_state_text(latest_heater_state) if latest_heater_state is not None else ""
            fig.add_annotation(
                text=f"<b>Current: {latest_temp:.1f}°C</b><br>Max: {monitor.max_temperature:.1f}°C<br>State: {heater_state_text}",
                xref="paper", yref="paper",
                x=0.52, y=0.95,
                xanchor="left",
                font=dict(size=16, color=COLORS['temperature']),
                showarrow=False,
            )
            
            # pH annotation
            fig.add_annotation(
                text=f"<b>Current: {latest_ph:.2f}</b><br>Range: {monitor.min_ph:.2f} - {monitor.max_ph:.2f}",
                xref="paper", yref="paper",
                x=0.02, y=0.45,
                xanchor="left",
                font=dict(size=16, color=COLORS['ph']),
                showarrow=False,
            )
        
        return fig