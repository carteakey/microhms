from flask import Flask
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from .models import db
from flask_login import LoginManager

import os

login_manager = LoginManager()


def create_app():
    # Load Environment Variables
    load_dotenv()

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URL"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
    app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024
    app.config["BOOTSTRAP_BOOTSWATCH_THEME"] = "Zephyr"
    app.config["BOOTSTRAP_SERVE_LOCAL"] = True

    # Bootstrap
    Bootstrap5(app)

    # DB
    db.init_app(app)

    csrf = CSRFProtect(app)

    migrate = Migrate(app, db, compare_type=True)

    login_manager.login_view = 'login.login'
    login_manager.init_app(app)

    with app.app_context():
            
        # blueprint for non-auth parts of app
        from .main import main as main
        
        app.register_blueprint(main)

        from project.invoice.routes import invoice_bp

        app.register_blueprint(invoice_bp)

        from project.login.routes import login_bp

        app.register_blueprint(login_bp)

    return app
