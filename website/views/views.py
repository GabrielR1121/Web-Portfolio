from flask import Blueprint, render_template, send_file
import json
from ..models.project import Project
from ..controls.github_request import get_project_info
import os
import threading


views = Blueprint("views", __name__)


# Define a context processor function to load JSON data
def load_base_data():
    with open("website/static/data/base.json", "r") as json_file:
        base_data = json.load(json_file)
    thread = threading.Thread(target=get_project_info)
    thread.start()
    return {"base_data": base_data}


# Register the context processor with Flask
@views.context_processor
def inject_page_data():
    return load_base_data()


# Creates a route to the home page
@views.route("/", methods=["GET"])
def home():
    with open("website/static/data/home.json", "r") as json_file:
        home_data = json.load(json_file)
    return render_template("home.html", home_data=home_data)


# Creates a route to download my resume
@views.route("/resume", methods=["GET"])
def resume():
    resume_path = f"static\documents\Resume Gabriel E Rodriguez Garcia.pdf"
    return send_file(resume_path, as_attachment=True)


# Creates a route to the awards page
@views.route("/awards", methods=["GET"])
def awards():
    with open("website/static/data/awards.json", "r") as json_file:
        award_data = json.load(json_file)
    return render_template("awards.html", award_data=award_data)


# Creates a route to the leadership page
@views.route("/leadership", methods=["GET"])
def leadership():
    with open("website/static/data/leadership.json", "r") as json_file:
        leadership_data = json.load(json_file)
    return render_template("leadership.html", leadership_data=leadership_data)


# Creates a route to the projects page
@views.route("/projects", methods=["GET"])
def projects():
    if os.path.exists("website/static/data/github.json"):

        with open("website/static/data/github.json", "r") as json_file:
            github_data = json.load(json_file)

        with open("website/static/data/project.json", "r") as json_file:
            project_data = json.load(json_file)

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

        return render_template("projects.html", projects=projects,project_data=project_data)
    else:
        return render_template("loading.html")


# Creates a route to the verify-data page. Used as a buffer if the GitHub API hasnt finished loading.
# When the data from the GitHub API is ready then return response of 200
# If data is not ready yet return responce of 404
@views.route("/verify-data", methods=["GET"])
def verify_data():
    if os.path.exists("website/static/data/github.json"):
        return "", 200
    else:
        return "", 404


# Creates a route the the work experience page
@views.route("/work-experience", methods=["GET"])
def work_experience():
    with open("website/static/data/work.json", "r") as json_file:
        work_data = json.load(json_file)
    return render_template("work_experience.html", work_data=work_data)
