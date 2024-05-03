from flask import Blueprint, render_template, send_file
import json
from ..models.project import Project
from ..controls.github_request import get_project_info
from ..config.config import base_filepath
import os

views = Blueprint("views", __name__)


def load_website_data():
    data = {}
    with open(base_filepath, "r") as json_file:
        data["base_data"] = json.load(json_file)

    for taskbar in data["base_data"]["taskbar"]:
        with open(taskbar["data_location"], "r") as json_file:
            data[taskbar["data_name"]] = json.load(json_file)

    get_project_info(data["project_data"]["request"])
    return data


@views.context_processor
def inject_page_data():
    return load_website_data()


@views.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@views.route("/resume", methods=["GET"])
def resume():
    resume_filepath = load_website_data()["home_data"]["resume"]["path"]
    return send_file(resume_filepath, as_attachment=True)


@views.route("/awards", methods=["GET"])
def awards():
    return render_template("awards.html")


@views.route("/leadership", methods=["GET"])
def leadership():
    return render_template("leadership.html")


@views.route("/projects", methods=["GET"])
def projects():
    git_path = load_website_data()["project_data"]["request"]["github_filepath"]
    pie_chart_path = load_website_data()["project_data"]["pie_chart"]["path"]
    if os.path.exists(git_path):
        with open(git_path, "r") as json_file:
            github_data = json.load(json_file)
        projects = {}
        for key, value in github_data.items():
            projects[key] = Project(
                value["name"],
                value["description"],
                value["created"],
                value["updated"],
                value["languages"],
                pie_chart_path,
            )
        return render_template("projects.html", projects=projects)
    else:
        return render_template("loading.html")


@views.route("/verify-data", methods=["GET"])
def verify_data():
    git_path = load_website_data()["project_data"]["request"]["github_filepath"]
    if os.path.exists(git_path):
        return "", 200
    else:
        return "", 404


@views.route("/work-experience", methods=["GET"])
def work_experience():
    return render_template("work_experience.html")
