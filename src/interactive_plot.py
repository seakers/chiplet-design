import dash
from dash import dcc, html, State
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os

class PlotLauncher:
    def __init__(self, file_path: str, x_axis: str, y_axis: str, sld_feat: list, color_feat: str, size_feat: str):
        self.app = dash.Dash("Dash app")
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

                html.Div([
                    "N_stack: ",
                    dcc.Input(id="input-1", type="number"),
                ]),
                html.Div([
                    "tsv_pitch: ",
                    dcc.Input(id="input-2", type="number"),
                ]),
                html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
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
                return ''
            N_stack = input1
            tsv_pitch = input2
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
            ai_model = 'densenet121'
            chip_arch = 'M3D'
            os.system('python submodules/HISIM/HISIM-IMC/analy_model.py --xbar_size %d \
                --N_stack %d\
                --N_tile %d \
                --N_tier %d \
                --N_pe %d \
                --freq_computing %f \
                --fclk_noc %f \
                --placement_method %d \
                --routing_method %d\
                --percent_router %f\
                --tsvPitch %f \
                --chip_architect %s\
                --W2d %d\
                --router_times_scale %d\
                --ai_model %s ' %(int(crossbar_size), int(N_stack), int(N_tile),int(N_tier),int(N_pe),float(f_core),float(f_noc),float(place_method),float(route_method),float(percent_router),float(tsv_pitch), str(chip_arch), int(W2d), int(router_times_scale), str(ai_model)))
                # Read the output from the file
            with open('Results/PPA.csv', 'r') as file:
                data = file.readlines()
                last_line = data[-1].strip().split(',')
                # power = float(last_line[11])/float(last_line[10])*pow(10,-3) # watts I think
                # print("Power: ", power)
                area = float(last_line[13]) # mm^2
                networkLatency = float(last_line[18]) # ns
                print("Area: ", area)
                print("Network Latency: ", networkLatency)
            return f'''
                Area: {area:.2f},\n
                Network Latency: {networkLatency:.2f}
            '''

    def load_data(self):
        """Loads the latest data from CSV."""
        try:
            df = pd.read_csv(self.file_path)
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return self.df  # Return last known dataframe if error occurs

    def run(self):
        """Runs the Dash app."""
        self.app.run_server(debug=True)

if __name__ == "__main__":
    app = PlotLauncher("Results/PPA.csv", "chip area (mm2)", "network_latency (ns)", ["3d NoC latency (ns)", "W3d"], "chip_Architecture", "W3d")
    app.run()
