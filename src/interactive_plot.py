import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, State
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os
import threading
import subprocess

class PlotLauncher:
    def __init__(self, file_path: str, x_axis: str, y_axis: str, sld_feat: list, color_feat: str, size_feat: str):
        self.app = dash.Dash("Dash app", external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.file_path = file_path
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.sld_feat = sld_feat
        self.color_feat = color_feat
        self.size_feat = size_feat

        # Load initial DataFrame
        self.df = self.load_data()

        # Define the app layout
        self.app.layout = html.Div(
            [
                html.H1("Interactive Scatter Plot", style={"textAlign": "center"}),
                
                html.Div(
                    dcc.Graph(id="scatter-plot"), 
                    style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center",
                        "height": "600px",  # Adjust height as needed
                    },
                ),

                # Auto-reload every 5 seconds
                dcc.Interval(id="interval-update", interval=5000, n_intervals=0),

                # Sliders Container (Side by Side)
                html.Div(
                    [
                        # First Slider
                        html.Div(
                            [
                                html.P(f"Filter by {self.sld_feat[0]}:", style={"textAlign": "center", "fontSize": 20}),
                                dcc.RangeSlider(
                                    id="a-slider",
                                    min=min(self.df[self.sld_feat[0]]),
                                    max=max(self.df[self.sld_feat[0]]),
                                    step=0.01,
                                    marks={
                                        min(self.df[self.sld_feat[0]]): str(f"{min(self.df[self.sld_feat[0]]):.2f}"),
                                        max(self.df[self.sld_feat[0]]): str(f"{max(self.df[self.sld_feat[0]]):.2f}")
                                    },
                                    value=[min(self.df[self.sld_feat[0]]), max(self.df[self.sld_feat[0]])],
                                ),
                            ],
                            style={"width": "48%", "padding": "10px"}  # Each slider takes 48% width
                        ),

                        # Second Slider
                        html.Div(
                            [
                                html.P(f"Filter by {self.sld_feat[1]}:", style={"textAlign": "center", "fontSize": 20}),
                                dcc.RangeSlider(
                                    id="b-slider",
                                    min=min(self.df[self.sld_feat[1]]),
                                    max=max(self.df[self.sld_feat[1]]),
                                    step=0.01,
                                    marks={
                                        min(self.df[self.sld_feat[1]]): str(f"{min(self.df[self.sld_feat[1]]):.2f}"),
                                        max(self.df[self.sld_feat[1]]): str(f"{max(self.df[self.sld_feat[1]]):.2f}")
                                    },
                                    value=[min(self.df[self.sld_feat[1]]), max(self.df[self.sld_feat[1]])],
                                ),
                            ],
                            style={"width": "48%", "padding": "10px"}  # Same width as first slider
                        ),
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",  # Space between sliders
                        "alignItems": "center",
                        "width": "80%",  # Adjust width of the container
                        "margin": "auto",  # Center the div
                    },
                ),

                html.Div(
                    [
                        # First Input (N_stack)
                        dbc.Row(
                            [
                                dbc.Col(html.Label("N_stack:", style={"fontSize": "18px", "fontWeight": "bold"}), width=2),
                                dbc.Col(dbc.Input(id="input-1", type="number", placeholder="Enter N_stack"), width=4),
                            ],
                            className="mb-3",
                        ),

                        # Second Input (tsv_pitch)
                        dbc.Row(
                            [
                                dbc.Col(html.Label("TSV Pitch:", style={"fontSize": "18px", "fontWeight": "bold"}), width=2),
                                dbc.Col(dbc.Input(id="input-2", type="number", placeholder="Enter TSV pitch"), width=4),
                            ],
                            className="mb-3",
                        ),

                        # Submit Button
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button("Submit", id="submit-button-state", n_clicks=0, color="primary", className="btn-lg"),
                                    width={"size": 3, "offset": 2},  # Centering the button
                                ),
                            ],
                            className="mt-3",
                        ),
                    ],
                    style={
                        "border": "2px solid #ddd",
                        "borderRadius": "10px",
                        "padding": "20px",
                        "boxShadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",
                        "width": "50%",
                        "margin": "auto",
                        "backgroundColor": "#f8f9fa",
                    },
                ),
                html.Div(id="number-output"),

            ],
            style={
                "width": "80%",
                "margin": "0 auto",
                "height": "auto",
                "border": "1px solid #ccc",
                "padding": "50px",
                "box-shadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",
            },
        )

        # Callback that updates the scatter plot
        @self.app.callback(
            Output("scatter-plot", "figure"),
            [
                Input("a-slider", "value"),
                Input("b-slider", "value"),
                Input("interval-update", "n_intervals"),  # Auto-refresh trigger
            ],
        )
        def update_scatter_plot(a_range, b_range, n_intervals):
            # Reload the DataFrame every interval
            df = self.load_data()

            # Unpack slider values
            a_low, a_high = a_range
            b_low, b_high = b_range

            # Apply filtering
            mask = (
                (df[self.sld_feat[0]] > a_low) & 
                (df[self.sld_feat[0]] < a_high) &
                (df[self.sld_feat[1]] > b_low) & 
                (df[self.sld_feat[1]] < b_high)
            )

            # Create scatter plot
            fig = px.scatter(
                df[mask],
                x=self.x_axis,
                y=self.y_axis,
                color=self.color_feat,
                size=self.size_feat,
                hover_data=df.columns,
            )

            fig.update_layout(width=800, height=600)
            return fig
        
        # callback that updates the scatter plot based on user input
        @self.app.callback(Output('number-output', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1', 'value'),
              State('input-2', 'value'))
        def update_output(n_clicks, input1, input2):
            if n_clicks == 0:
                return ""
            threading.Thread(target=self.run_hisim_analysis, args=(input1, input2)).start()

            return "Processing... Results will be updated soon!"

    def load_data(self):
        """Loads the latest data from CSV."""
        try:
            df = pd.read_csv(self.file_path)
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return self.df  # Return last known dataframe if error occurs
        
    def run_hisim_analysis(self, N_stack, tsv_pitch):
        """Runs the external analysis asynchronously."""
        crossbar_size = 1024
        N_tile = 36
        N_tier = 3
        N_pe = 1
        f_core = 1
        f_noc = 5
        place_method = 2
        route_method = 1
        percent_router = 1
        W2d = 32
        router_times_scale = 1
        ai_model = "densenet121"
        chip_arch = "M3D"

        cmd = f"python submodules/HISIM/HISIM-IMC/analy_model.py --xbar_size {crossbar_size} \
            --N_stack {N_stack} --N_tile {N_tile} --N_tier {N_tier} --N_pe {N_pe} \
            --freq_computing {f_core} --fclk_noc {f_noc} --placement_method {place_method} \
            --routing_method {route_method} --percent_router {percent_router} \
            --tsvPitch {tsv_pitch} --chip_architect {chip_arch} --W2d {W2d} \
            --router_times_scale {router_times_scale} --ai_model {ai_model}"

        # Run in a separate thread (non-blocking)
        subprocess.Popen(cmd, shell=True)

        # Update the DataFrame with the new results
        self.df = self.load_data()

    def run(self):
        """Runs the Dash app."""
        self.app.run_server(debug=True)

if __name__ == "__main__":
    app = PlotLauncher("Results/PPA.csv", "chip area (mm2)", "network_latency (ns)", ["3d NoC latency (ns)", "W3d"], "chip_Architecture", "W3d")
    app.run()
