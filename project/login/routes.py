from functools import wraps
from project import login_manager

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from flask_login import login_user, login_required, logout_user, current_user

from project.login.forms import LoginForm, RegisterForm

from project.models import User, Role, RoleAssignment, db

from werkzeug.security import check_password_hash, generate_password_hash

login_bp = Blueprint(
    "login", __name__, template_folder="templates", static_folder="static"
)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# RBAC
def role_required(role: str):
    def _role_required(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            print (current_user.is_authenticated)
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if not current_user.has_role(role):
                abort(403)
            return f(*args, **kwargs)

        return decorated_view

    return _role_required


def roles_required(roles: list, require_all=False):
    def _roles_required(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            if len(roles) == 0:
                raise ValueError("Empty list used when requiring a role.")
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if require_all and not all(current_user.has_role(role) for role in roles):
                return "Forbidden", 403
            elif not require_all and not any(
                current_user.has_role(role) for role in roles
            ):
                return "Forbidden", 403
            return f(*args, **kwargs)

        return decorated_view

    return _roles_required


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You are now logged in. Welcome back!", "success")
                return redirect(request.args.get("next") or url_for("main.homepage"))
            else:
                flash("Incorrect password. Please try again.", "danger")
        else:
            flash("No user found. Please try again.", "danger")

    return render_template("login.html", form=form)


@login_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login.login"))

@login_bp.route("/register", methods=["GET", "POST"])
@login_required
@role_required("admin")
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data,active=True)

        db.session.add(new_user)
        db.session.commit()

        # Create Role if it doesn't exist
        role = Role.query.filter_by(name="admin").first()
        if not role:
            role = Role(name="admin")
            db.session.add(role)
            db.session.commit()

        role = Role.query.filter_by(name="user").first()
        if not role:
            role = Role(name="user")
            db.session.add(role)
            db.session.commit()

        # Assign Role to User
        if form.role.data:
            role = Role.query.filter_by(name=form.role.data).first()
            RoleAssignment.create(role_name=role.name, user_id=new_user.id)

        flash("You have successfully registered. Please login.", "success")
        return redirect(url_for("login.login"))

    return render_template("register.html", form=form)
