
from flask import Blueprint,render_template

main = Blueprint("main", __name__, template_folder="templates", static_folder="static")

@main.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("404.html", error=e), 404

@main.route("/", methods=["GET", "POST"])
def homepage():
    """
    homepage route
    """
    return render_template("homepage.html")

