from project import login_manager

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from flask_login import login_user, login_required, logout_user, current_user

from project.login.forms import LoginForm, RegisterForm

from project.models import User, db

from werkzeug.security import check_password_hash, generate_password_hash

login_bp = Blueprint(
    "login", __name__, template_folder="templates", static_folder="static"
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
@login_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("main.homepage"))
    return render_template("login.html", form=form)


@login_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login.login"))


@login_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login.login"))

    return render_template("register.html", form=form)
