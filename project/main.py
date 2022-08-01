from flask import Blueprint, render_template

main = Blueprint("main", __name__, template_folder="templates", static_folder="static")


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html", error=e), 404


@main.app_errorhandler(403)
def forbidden(e):
    return render_template("404.html", error=e), 403


@main.route("/", methods=["GET", "POST"])
def homepage():
    """
    homepage route
    """
    return render_template("homepage.html")
