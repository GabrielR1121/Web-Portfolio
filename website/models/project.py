import json
import plotly
from ..controls import graphs
from datetime import datetime


# This class is to process the data from the projects collected from the GitHub API
class Project:
    #  Each Project class will have the:
    #  * NAME of the repository
    #  * DESCRIPTION of the repository
    #  * The date the repository was CREATED
    #  * The date the repository was last UPDATED
    #  * A dictionary of the LANGUAGE distribution of the repository
    #  * The DATA dictionary will hold the processed data from the language dictionary
    def __init__(self, name, description, created_at, updated_at, languages,pie_path):
        self.name = name
        self.description = description
        self.created = self.convert_to_date(created_at)
        self.updated = self.convert_to_date(updated_at)
        self.languages = {language: int(value) for language, value in languages.items()}
        self.pie_path = pie_path
        self.data = {}

    # Calculates the percentage values of languages used in the project
    def calc_chart_data(self):
        total = sum(self.languages.values())
        self.data = {
            key: (value / total) * 100 for key, value in self.languages.items()
        }

    # Creates the Jsonified pie chart ready for it to be displayed
    def create_chart(self):
        self.calc_chart_data()

        # Calls the pie_chart method in the graphs.py file in order to create the pie chart
        return json.dumps(
            graphs.pie_chart(list(self.data.keys()), list(self.data.values()), self.pie_path),
            cls=plotly.utils.PlotlyJSONEncoder,
        )

    # Converts the raw date from the GitHub API into a more readable date
    def convert_to_date(self, date):
        # Convert string to datetime object
        datetime_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")

        # Format the datetime object
        formatted_date = datetime_obj.strftime("%B %d, %Y")

        return formatted_date
