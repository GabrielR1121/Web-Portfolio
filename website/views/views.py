from flask import Blueprint, render_template, send_file

views = Blueprint("views", __name__)


# Creates a route to the home page
@views.route("/", methods=["GET"])
def home():
    return render_template("home.html")


# Creates a route to download my resume
@views.route("/resume", methods=["GET"])
def resume():
    resume_path = f"static\documents\Resume Gabriel E Rodriguez Garcia.pdf"
    return send_file(resume_path, as_attachment=True)


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
    return render_template("projects.html")


# Creates a route the the work experience page
@views.route("/work-experience", methods=["GET"])
def work_experience():
    return render_template("work_experience.html")
