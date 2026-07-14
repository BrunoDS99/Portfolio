from flask import Flask, render_template
from project_loader import load_projects

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/projects")
def projects():
    return render_template("projects.html", projects=load_projects())

@app.route("/projects/<slug>")
def project(slug):

    projects = load_projects()

    project = next(
        (p for p in projects if p["slug"] == slug),
        None
    )

    if project is None:
        return render_template("404.html"), 404

    return render_template(
        "project.html",
        project=project
    )


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)