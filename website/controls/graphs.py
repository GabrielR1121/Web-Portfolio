import plotly.graph_objects as go


def pie_chart(languages, values, title=""):
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

    # Sets the title and the width and height of the pie chart
    fig.update_layout(title_text=title, width=350, height=400)

    return fig
