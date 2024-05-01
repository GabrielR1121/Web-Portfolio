import plotly.graph_objects as go
import json


def pie_chart(languages, values):
    """
    Creates the Pie Chart that displays the language distribution within each repo
    """


    # Create the Pie chart
    fig = go.Figure(
        data=[
            go.Pie(
                labels=languages,
                values=values,
            )
        ],
    )

    # Sets the pie chart to the correct settings
    fig.update_layout( get_chart_settings() )

    return fig

# Gets the settings in the pie_chart.json 
def get_chart_settings():
    with open("website/static/data/pie_chart.json", "r") as json_file:
        return json.load(json_file)
