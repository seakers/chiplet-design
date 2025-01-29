from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash("Dash app")

app.layout = html.Div(
    [
        html.H4("Interactive scatter plot with Iris dataset", style={"textAlign": "center"}),  # Center-align the header
        html.Div(
            dcc.Graph(id="scatter-plot"), 
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "height": "600px",  # Adjust this as needed
            },
        ),
        html.P("Filter by petal width:", style={"textAlign": "center"}),  # Center-align the paragraph
        html.Div(
            dcc.RangeSlider(
                id="range-slider",
                min=0,
                max=2.5,
                step=0.01,
                marks={0: "0", 2.5: "2.5"},
                value=[0.5, 2],
            ),
            style={  # Add padding next to the slider
                "padding-left": "80px",
                "padding-right": "80px",  # Add padding around the slider
            },
        ),
    ],
    style={
        "width": "80%",  # Set the width to 80% of the parent container
        "margin": "0 auto",  # Center the div horizontally
        "height": "800px",  # Set a specific height (optional)
        "border": "1px solid #ccc",  # Optional: Add a border for visibility
        "padding": "20px",  # Add padding inside the div
        "box-shadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",  # Optional: Add a shadow for styling
    },
)

@app.callback(
    Output("scatter-plot", "figure"),
    Input("range-slider", "value"),
)
def update_bar_chart(slider_range):
    df = px.data.iris()  # Replace with your own data source
    low, high = slider_range
    mask = (df["petal_width"] > low) & (df["petal_width"] < high)
    fig = px.scatter(
        df[mask],
        x="sepal_width",
        y="sepal_length",
        color="species",
        size="petal_length",
        hover_data=["petal_width"],
    )
    # Update layout for aspect ratio
    fig.update_layout(
        width=800,  # Set width in pixels
        height=600,  # Set height in pixels
        xaxis=dict(scaleanchor="y", title="Sepal Width"),
        yaxis=dict(title="Sepal Length"),
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)