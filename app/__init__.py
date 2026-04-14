import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFError, CSRFProtect

from config import Config, assert_db_not_localhost_in_cloud

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
csrf = CSRFProtect()

from app import models as _models  # noqa: E402, F401 — registra tablas en metadata


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    assert_db_not_localhost_in_cloud(app.config["SQLALCHEMY_DATABASE_URI"])

    os.makedirs(os.path.join(app.root_path, "static", "generated"), exist_ok=True)

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    csrf.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import main_bp, auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template("errors/400.html", mensaje=str(e)), 400

    @app.errorhandler(404)
    def not_found(_e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(_e):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    with app.app_context():
        db.create_all()
        from app import seed

        seed.seed_curated_reflections()

    return app
