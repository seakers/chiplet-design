from dash import Dash, dcc, html, Input, Output
import plotly.express as px

class PlotLauncher():
    def __init__(self, df, x_axis: str, y_axis: str, sld_feat: list, color_feat: str, size_feat: str):
        self.app = Dash("Dash app")
        self.df = df
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.sld_feat = sld_feat
        self.color_feat = color_feat
        self.size_feat = size_feat

        # Define the app layout
        self.app.layout = html.Div(
            [
                html.H1(
                    "Interactive scatter plot with Chiplet Design Results", 
                    style={"textAlign": "center"}
                ),
                html.Div(
                    dcc.Graph(id="scatter-plot"), 
                    style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center",
                        "height": "600px",  # Adjust height as needed
                    },
                ),
                html.P(f"Filter by {self.sld_feat[0]}:", style={"textAlign": "center"}),
                html.Div(
                    dcc.RangeSlider(
                        id="a-slider",
                        min=min(self.df[self.sld_feat[0]]), # Adjust these values based on your data range
                        max=max(self.df[self.sld_feat[0]]),
                        step=0.01,
                        marks={min(self.df[self.sld_feat[0]]): str(min(self.df[self.sld_feat[0]])), max(self.df[self.sld_feat[0]]): str(max(self.df[self.sld_feat[0]]))},
                        value=[min(self.df[self.sld_feat[0]]), max(self.df[self.sld_feat[0]])],
                    ),
                    style={
                        "padding-left": "80px",
                        "padding-right": "80px",
                    },
                ),
                html.P(f"Filter by {self.sld_feat[1]}:", style={"textAlign": "center"}),
                html.Div(
                    dcc.RangeSlider(
                        id="b-slider",
                        min=min(self.df[self.sld_feat[1]]), # Adjust these values based on your data range
                        max=max(self.df[self.sld_feat[1]]),
                        step=0.01,
                        marks={min(self.df[self.sld_feat[1]]): str(min(self.df[self.sld_feat[1]])), max(self.df[self.sld_feat[1]]): str(max(self.df[self.sld_feat[1]]))},
                        value=[min(self.df[self.sld_feat[1]]), max(self.df[self.sld_feat[1]])],
                    ),
                    style={
                        "padding-left": "80px",
                        "padding-right": "80px",
                    },
                ),
            ],
            style={
                "width": "80%", # 80% width of the parent container
                "margin": "0 auto", # Center horizontally
                "height": "auto",
                "border": "1px solid #ccc", # Optional border
                "padding": "50px", # Inner padding
                "box-shadow": "2px 2px 10px rgba(0, 0, 0, 0.1)", # Optional shadow
            },
        )

        # Callback that updates the scatter plot based on the slider values
        @self.app.callback(
            Output("scatter-plot", "figure"),
            [Input("a-slider", "value"),
             Input("b-slider", "value")]
        )
        def update_scatter_plot(a_range, b_range):
            # Unpack the slider ranges
            a_low, a_high = a_range
            b_low, b_high = b_range

            # Create a mask that filters based on petal width and petal length
            mask = (
                (self.df[self.sld_feat[0]] > a_low) & 
                (self.df[self.sld_feat[0]] < a_high) &
                (self.df[self.sld_feat[1]] > b_low) & 
                (self.df[self.sld_feat[1]] < b_high)
            )

            # Create the scatter plot with the filtered data
            fig = px.scatter(
                self.df[mask],
                x=self.x_axis,
                y=self.y_axis,
                color=self.color_feat,
                size=self.size_feat,
                hover_data=df.columns,
            )

            # Update layout settings (optional)
            fig.update_layout(
                width=800,
                height=600,
            )

            return fig

    def run(self):
        self.app.run_server(debug=True)
