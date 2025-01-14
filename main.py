import dash
from pressure_monitor import PressureMonitor
from layout import create_layout
from callbacks import register_callbacks

def main():
    app = dash.Dash(__name__, suppress_callback_exceptions=True)
    monitor = PressureMonitor(window_size=100)
    
    app.layout = create_layout()
    register_callbacks(app, monitor)
    
    try:
        app.run_server(debug=False)
    finally:
        monitor.cleanup()

if __name__ == '__main__':
    main()