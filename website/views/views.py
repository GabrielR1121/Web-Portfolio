from flask import Blueprint, render_template, send_file
import json
from ..models.project import Project
from ..controls.github_request import get_project_info
from ..config.config import get_config
import os
from datetime import datetime

# Define the blueprint
views = Blueprint("views", __name__)


def load_website_data():
    data = {}
    config = get_config()
    base_filepath = config.BASE_FILEPATH

    # Load base data
    with open(base_filepath, "r") as json_file:
        data["base_data"] = json.load(json_file)

    # Load taskbar data
    for taskbar in data["base_data"]["taskbar"]:
        with open(taskbar["data_location"], "r") as json_file:
            data[taskbar["data_name"]] = json.load(json_file)

    # Process repo data
    repo_data = get_project_info(data["project_data"]["request"])
    try:
        # Update last_updated in base data
        first_key = next(iter(repo_data["projects"]))  # Get the first key
        first_value = repo_data["projects"][
            first_key
        ]  # Get the value associated with the first key
        data["base_data"]["last_updated"] += convert_to_date(first_value["updated"])

        # Write updated base data back to file
        with open(base_filepath, "w") as f:
            json.dump(data["base_data"], f, indent=3)
    except Exception as e:
        data["base_data"]["last_updated"] += "TBD"
        print(f"Error: {e}")

    return data


# Converts the raw date from the GitHub API into a more readable date
def convert_to_date(date):
    # Convert string to datetime object
    datetime_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")

    # Format the datetime object
    formatted_date = datetime_obj.strftime("%B %d, %Y")

    return formatted_date


# Context processor to inject data into templates
@views.context_processor
def inject_page_data():
    return load_website_data()


# Route for the home page
@views.route("/", methods=["GET"])
def home():
    return render_template("home.html")


# Route to download the resume
@views.route("/resume", methods=["GET"])
def resume():
    resume_filepath = load_website_data()["home_data"]["resume"]["path"]
    return send_file(resume_filepath, as_attachment=True)


# Route to the awards page
@views.route("/awards", methods=["GET"])
def awards():
    return render_template("awards.html")


# Route to the leadership page
@views.route("/leadership", methods=["GET"])
def leadership():
    return render_template("leadership.html")


# Route to the projects page
@views.route("/projects", methods=["GET"])
def projects():
    git_path = load_website_data()["project_data"]["request"]["github_filepath"]
    pie_path = load_website_data()["project_data"]["pie_chart"]["path"]
    if os.path.exists(git_path):
        with open(git_path, "r") as json_file:
            github_data = json.load(json_file)
        projects = {}

        for key, value in github_data["projects"].items():
            if not value["ignore"]:
                projects[key] = Project(
                    value["name"],
                    value["description"],
                    value["created"],
                    value["updated"],
                    value["languages"],
                    pie_path,
                )
        return render_template("projects.html", projects=projects)
    else:
        return render_template("loading.html")


# Route to verify data availability
@views.route("/verify-data", methods=["GET"])
def verify_data():
    git_path = load_website_data()["project_data"]["request"]["github_filepath"]
    if os.path.exists(git_path):
        return "", 200
    else:
        return "", 404


# Route to the work experience page
@views.route("/work-experience", methods=["GET"])
def work_experience():
    return render_template("work_experience.html")
