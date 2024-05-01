from flask import Blueprint, render_template, send_file
import json
from ..models.project import Project
from ..controls.github_request import get_project_info
from ..config.config import base_filepath, resume_filepath, github_filepath
import os


views = Blueprint("views", __name__)
data = {}


# Define a context processor function to load JSON data
def load_website_data():
    get_project_info()

    with open(base_filepath, "r") as json_file:
        data["base_data"] = json.load(json_file)

    for taskbar in data["base_data"]["taskbar"]:
        with open(taskbar["data_location"], "r") as json_file:
            data[taskbar["data_name"]] = json.load(json_file)

    return data


# Register the context processor with Flask
@views.context_processor
def inject_page_data():
    return load_website_data()


# Creates a route to the home page
@views.route("/", methods=["GET"])
def home():
    return render_template("home.html")


# Creates a route to download my resume
@views.route("/resume", methods=["GET"])
def resume():
    return send_file(resume_filepath, as_attachment=True)


# Creates a route to the awards page
@views.route("/awards", methods=["GET"])
def awards():
    return render_template("awards.html")


# Creates a route to the leadership page
@views.route("/leadership", methods=["GET"])
def leadership():
    return render_template("leadership.html")


# Creates a route to the projects page
@views.route("/projects", methods=["GET"])
def projects():
    if os.path.exists(github_filepath):

        with open(github_filepath, "r") as json_file:
            github_data = json.load(json_file)

        # Parse JSON data into objects
        projects = {}
        for key, value in github_data.items():
            projects[key] = Project(
                value["name"],
                value["description"],
                value["created"],
                value["updated"],
                value["languages"],
            )

        return render_template("projects.html", projects=projects)
    else:
        return render_template("loading.html")


# Creates a route to the verify-data page. Used as a buffer if the GitHub API hasnt finished loading.
# When the data from the GitHub API is ready then return response of 200
# If data is not ready yet return responce of 404
@views.route("/verify-data", methods=["GET"])
def verify_data():
    if os.path.exists(github_filepath):
        return "", 200
    else:
        return "", 404


# Creates a route the the work experience page
@views.route("/work-experience", methods=["GET"])
def work_experience():
    return render_template("work_experience.html")
